import os
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.conf import settings
import numpy as np
from .opencv_detection_utils.FaceDetector import FaceDetector
from .streaming_service import Streamer
from io import BytesIO
import cv2
from .camera_service.camera_pi import Camera

face_path = settings.BASE_DIR / 'pi_stream' / 'face-config'
proto_path = str(face_path / 'deploy.prototxt')
model_path = str(face_path / 'res10_300x300_ssd_iter_140000.caffemodel')
#detector = HumanDetector(scale=1.065, win_stride=(8, 8))
detector = FaceDetector(proto_path, model_path, confidence=0.2)
streamer = Streamer(Camera(), detector)

def detect(image):
   detected = detector.detect_image(image)
   _, frame = cv2.imencode('.JPEG', detected.get_image())
   return frame.tostring()

def stream(request):
    return(render(
        request,
        'pi_stream/stream.html'
    ))
    
def video_feed(request):   
    streamer = Streamer(Camera(), detector)
    return(StreamingHttpResponse(
        streamer.stream(), 
        content_type='multipart/x-mixed-replace; boundary=frame'
    ))
