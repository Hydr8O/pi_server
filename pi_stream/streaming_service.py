from .Streamer import Streamer
from .image_encoding_service import image_from_bytes, image_to_bytes
from .Alarm import Alarm

def stream_detections(camera, detector):
    '''Streams frames with detections from camera'''
    streamer = Streamer(camera)
    alarm = Alarm(frames_with_no_detections_threshold=30, melody='ring.wav')
    for frame in streamer.stream():
        frame_with_detections = _detect_objects_on_frame(detector, frame)
        alarm.perform_alarm_cycle(detector.is_object())
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
        
    
