import os
class Alarm:
    '''Alarm which is _sounded when an object has been detected'''
    def __init__(self, frames_with_no_detections_threshold, melody):
        self._frames_with_no_detections_threshold = frames_with_no_detections_threshold
        self._frames_with_no_detections = 0
        self._is_ready_to_sound = True
        self._melody = melody
    
    def perform_alarm_cycle(self, is_object):
        '''Performs an alarm cycle including _refreshing and _sounding'''
        if self._is_needed_to_refresh():
            self._refresh()
            
        if is_object == True:
            self._set_frames_with_no_detections_to_zero()
            self._perform_sound_cycle()
        else:
            self._increment_frames_with_no_detections()
    
    def _perform_sound_cycle(self):
        '''_Sounds an alarm and puts it on cooldown if it is ready to _sound'''
        if self._is_ready_to_sound == True:
            self._sound()
            self._is_ready_to_sound = False
    
    def _increment_frames_with_no_detections(self):
        '''Increments frames with no detections count'''
        self._frames_with_no_detections += 1
    
    def _is_needed_to_refresh(self):
        '''Checks if frames with no detections count has reached theshold'''
        if self._frames_with_no_detections == self._frames_with_no_detections_threshold:
            return True
        else:
            return False
    
    def _sound(self):
        '''Sounds the alarm''' 
        os.system(f'omxplayer -o local {self._melody} &')
             
    def _set_frames_with_no_detections_to_zero(self):
        self._frames_with_no_detections = 0
    
    def _refresh(self):
        '''Refreshes the alarm so it rings on the next detection'''
        self._is_ready_to_sound = True
        self._set_frames_with_no_detections_to_zero()
