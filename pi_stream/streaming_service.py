from datetime import datetime
from django.core.files.base import ContentFile
from django.apps import apps
from .Streamer import Streamer
from .image_encoding_service import image_from_bytes, image_to_bytes
from .Alarm import Alarm

def stream_detections(camera, detector):
    '''Streams frames with detections from camera'''
    streamer = Streamer(camera)
    alarm = Alarm(frames_with_no_detections_threshold=30, melody='ring.wav')
    for frame in streamer.stream():
        frame_with_detections = _detect_objects_on_frame(detector, frame)
        perform_alarm_cycle(alarm, frame_with_detections, detector.is_object())
        yield _construct_next_frame(frame_with_detections)
 
def stream(camera):
    '''Streams frames from camera'''
    streamer = Streamer(camera)
    for frame in streamer.stream():
        yield _construct_next_frame(frame)
    
           
def _detect_objects_on_frame(detector, frame):
    '''Detects objects on the current frame''' 
    image = image_from_bytes(frame)
    detected = detector.detect_image(image, crop=(700, 350, 500, 300))
    return image_to_bytes(detected, '.JPEG')

def _construct_next_frame(frame):
    '''Turns frame insto the right format and returns it'''
    return (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
    
def perform_alarm_cycle(alarm, frame_with_detections, is_object):
     '''Performs an alarm cycle including refreshing and sounding'''
     if alarm._is_needed_to_refresh():
         alarm._refresh()
     if is_object == True:
         alarm._set_frames_with_no_detections_to_zero()
         if alarm._is_ready_to_sound == True:
            perform_sound_cycle(alarm)
            save_detection_to_db(frame_with_detections)
     else:
         alarm._increment_frames_with_no_detections()

def perform_sound_cycle(alarm):
     '''Sounds an alarm and puts it on cooldown'''
     alarm._sound()
     alarm._is_ready_to_sound = False

def save_detection_to_db(frame_with_detections):
     timestamp = str(datetime.now())
     visitor_detection = apps.get_model('pi_visitors', 'VisitorDetection')
     visitor_detection.objects.create(image=ContentFile(content=frame_with_detections, name=timestamp))
