import os
from django.shortcuts import render
from django.http import StreamingHttpResponse
import numpy as np
from .opencv_detection_utils.HumanDetector import HumanDetector
from .streaming_service import Streamer
from io import BytesIO
import cv2
from .camera_service.camera_pi import Camera

detector = HumanDetector(scale=1.065, win_stride=(8, 8))
streamer = Streamer(Camera())

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
    return(StreamingHttpResponse(
        streamer.stream(), 
        content_type='multipart/x-mixed-replace; boundary=frame'
    ))
