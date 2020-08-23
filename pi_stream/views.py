import os
from django.shortcuts import render
from django.http import StreamingHttpResponse
import numpy as np
from opencv_detection_utils.HumanDetector import HumanDetector
from io import BytesIO
import cv2
from camera_pi import Camera

detector = HumanDetector(scale=1.065, win_stride=(8, 8))

def detect(image):
   detected = detector.detect_image(image)
   _, frame = cv2.imencode('.JPEG', detected.get_image())
   return frame.tostring()

def stream(request):
    return(render(
        request,
        'pi_stream/stream.html'
    ))

human_spotted = False
false_frames = 0
def gen(camera):
    global human_spotted
    global false_frames
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        image = cv2.imdecode(np.frombuffer(frame, np.uint8), 1)
        frame = detect(image)
        is_human = detector.is_human()
        if false_frames == 30:
           human_spotted = False
           false_frames = 0

        if is_human == True:
           false_frames = 0
           if human_spotted == False:
              os.system('omxplayer -o local ring.mp3 &')
              human_spotted = True
              print(is_human)
        else:
           false_frames += 1
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
def video_feed(request):
    return(StreamingHttpResponse(
        gen(Camera()), 
        content_type='multipart/x-mixed-replace; boundary=frame'
    ))
