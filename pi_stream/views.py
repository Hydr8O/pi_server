import os
import threading
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.conf import settings
import numpy as np
from .opencv_detection_utils.FaceDetector import FaceDetector
from .opencv_detection_utils.HumanDetector import HumanDetector
from .streaming_service import Streamer
from io import BytesIO
import cv2
from .camera_service.camera_pi import Camera

face_path = settings.BASE_DIR / 'pi_stream' / 'face-config'
proto_path1 = str(face_path / 'deploy.prototxt')
proto_path2 = str(face_path / 'deploy.prototxt2')
model_path1 = str(face_path / 'res10_300x300_ssd_iter_140000.caffemodel')
model_path2 = str(face_path / 'res10_300x300_ssd_iter_140000.caffemodel2')
detectors = {"detector1": False, "detector2": False}
detector1 = FaceDetector(proto_path1, model_path1, confidence=.2)
detector2 = FaceDetector(proto_path2, model_path2, confidence=.2)
#detector = HumanDetector()
def detect(image):
   detected = detector.detect_image(image)
   _, frame = cv2.imencode('.JPEG', detected.get_image())
   return frame.tostring()

def stream(request):
    return(render(
        request,
        'pi_stream/stream.html'
    ))
    
def video_feed(response):   
    if detectors["detector1"] == False:
        detectors["detector2"] = False
        streamer = Streamer(Camera(), detector1)
        detectors["detector1"] = True
    else:
        detectors["detector1"] = False
        streamer = Streamer(Camera(), detector2)
        detectors["detector2"] = True
    return(StreamingHttpResponse(
        streamer.stream(), 
        content_type='multipart/x-mixed-replace; boundary=frame'
    ))

video_feed('-')
