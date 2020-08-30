from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.conf import settings
from .opencv_detection_utils.FaceDetector import FaceDetector
from .camera_service.camera_pi import Camera
from .Alarm import Alarm
from .streaming_service import stream_detections

proto_path = str(settings.FACE_PATH / 'deploy.prototxt')
model_path = str(settings.FACE_PATH / 'res10_300x300_ssd_iter_140000.caffemodel')
alarm = Alarm(
    frames_with_no_detections_threshold=30, 
    melody='ring.wav'
)

def stream(request):
    return(render(
        request,
        'pi_stream/stream.html'
    ))
    
def video_feed(response):
    detector = FaceDetector(proto_path, model_path, confidence=.4)
    return(StreamingHttpResponse(
        stream_detections(Camera(), detector, alarm), 
        content_type='multipart/x-mixed-replace; boundary=frame'
    ))
