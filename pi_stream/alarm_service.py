import os
class Alarm:
    '''Alarm which is sounded when an object has been detected'''
    def __init__(self, frames_with_no_detections_threshold):
        self._frames_with_no_detections_threshold = frames_with_no_detections_threshold
        self._frames_with_no_detections = 0
        self._is_ready_to_sound = True
    
    def increment_frames_with_no_detections(self):
        '''Increments frames with no detections count'''
        self._frames_with_no_detections += 1
    
    def is_needed_to_refresh(self):
        '''Checks if frames with no detections count has reached theshold'''
        if self._frames_with_no_detections == self._frames_with_no_detections_threshold:
            return True
        else:
            return False
    
    def sound(self):
        '''Sounds the alarm''' 
        if self._is_ready_to_sound == True:
            os.system('omxplayer -o local ring.mp3 &')
            self._is_ready_to_sound = False      
               
    def set_frames_with_no_detections_to_zero(self):
        self._frames_with_no_detections = 0
    
    def refresh(self):
        '''Refreshes the alarm so it rings on the next detection'''
        self._is_ready_to_sound = True
        self.set_frames_with_no_detections_to_zero()
        
