import cv2
from .opencv_detection_utils.HumanDetector import HumanDetector
from .image_encoding_service import image_to_bytes, image_from_bytes
from .alarm_service import Alarm

class Streamer:
    '''Takes frames from the camera and processes them''' 
    def __init__(self, camera, detector, frames_with_no_detections_threshold=30):
        self._camera = camera
        self._current_frame = None
        self._alarm = Alarm(frames_with_no_detections_threshold)
        self._detector = detector
    
    def stream(self):
        '''Starts to stream video from camera'''
        while True:
            self._set_current_frame()
            self._draw_detections_on_current_frame()
            
            if self._alarm.is_needed_to_refresh():
                self._alarm.refresh()
                
            if self._detector.is_object() == True:
                self._alarm.set_frames_with_no_detections_to_zero()
                self._alarm.sound()
            else:
                self._alarm.increment_frames_with_no_detections()
    
            next_frame = self._construct_next_frame()
            yield next_frame
    

    def _process_frame(self):
        self._set_current_frame()
        self._draw_detections_on_current_frame()
            
        if self._alarm.is_needed_to_refresh():
            self._alarm.refresh()
                
        if self._detector.is_human() == True:
            self._alarm.set_frames_with_no_detections_to_zero()
            self._alarm.sound()
        else:
            self._alarm.increment_frames_with_no_detections()
    
    def start_frame_processing(self):
        '''Root stream which always works'''
        while True:
            print('streaming')
            self._set_current_frame()
            self._draw_detections_on_current_frame()
            
            if self._alarm.is_needed_to_refresh():
                self._alarm.refresh()
                
            if self._detector.is_object() == True:
                self._alarm.set_frames_with_no_detections_to_zero()
                self._alarm.sound()
            else:
                self._alarm.increment_frames_with_no_detections()
    

    def _set_current_frame(self):
        '''Gets frame from camera and sets it as current frame'''
        self._current_frame = self._camera.get_frame()
                    
    def _draw_detections_on_current_frame(self):
        '''Draws detected objects on the current frame''' 
        image = image_from_bytes(self._current_frame)
        detected = self._detector.detect_image(image, crop=(700, 350, 500, 300))
        self._current_frame = image_to_bytes(detected, '.JPEG')
        
    def _construct_next_frame(self):
        return (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + self._current_frame + b'\r\n')
