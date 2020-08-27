import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from alarm_service import Alarm
import os

def test_increment_frames_with_no_detections():
    alarm = Alarm(frames_with_no_detections_threshold=5, melody='ring.mp3')
    alarm._increment_frames_with_no_detections()
    assert alarm._frames_with_no_detections == 1

def test_refresh_frames_with_no_detections():
    alarm = Alarm(frames_with_no_detections_threshold=5, melody='ring.mp3')
    alarm._increment_frames_with_no_detections()
    alarm._refresh()
    assert alarm._frames_with_no_detections == 0
    
def test_refresh_is_ready_to_sound():
    alarm = Alarm(frames_with_no_detections_threshold=5, melody='ring.mp3')
    alarm._is_ready_to_sound = False
    alarm._refresh()
    assert alarm._is_ready_to_sound == True
    
def test_is_needed_to_refresh_threshold_not_reached():
    alarm = Alarm(frames_with_no_detections_threshold=5, melody='ring.mp3')
    assert alarm._is_needed_to_refresh() == False
    
def test_is_needed_to_refresh_threshold_reached():
    alarm = Alarm(frames_with_no_detections_threshold=5, melody='ring.mp3')
    alarm._frames_with_no_detections = 5
    assert alarm._is_needed_to_refresh() == True
    
def test_set_frames_with_no_detections_to_zero():
    alarm = Alarm(frames_with_no_detections_threshold=5, melody='ring.mp3')
    alarm._frames_with_no_detections = 4
    alarm._set_frames_with_no_detections_to_zero()
    assert alarm._frames_with_no_detections == 0
    
def test_not_ready_after_sound_cycle():
    alarm = Alarm(frames_with_no_detections_threshold=5, melody='ring.mp3')
    alarm._is_ready_to_sound = True
    alarm._perform_sound_cycle()
    assert alarm._is_ready_to_sound == False
    
    