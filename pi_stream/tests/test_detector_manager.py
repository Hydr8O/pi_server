class DetectorManager:
    '''Decides which detector should be used for a client'''
    def __init__(self, detectors, streamers):
        self.detectors = detectors
        self.streamers = streamers
        self._current_detector_index = 0
        #[{'detector': detector, 'status': 'free'}]
    def get_free_detector(self):
        for detector in self.detectors:
            if detector['status'] == 'free':
                detector['status'] = 'busy'
                return detector['detector']

    def add_streamer(self, streamer):
        self.streamers.append(streamer)
def test_get_free_detector_first_free():
    manager = DetectorManager(detectors=[{'detector': 1, 'status': 'free'}])
    assert manager.get_free_detector() == 1    
    
def test_get_free_detector_second_free():
    manager = DetectorManager([
        {'detector': 1, 'status': 'busy'}, 
        {'detector': 2, 'status': 'free'}
    ])
    assert manager.get_free_detector() == 2   
    
def test_make_detector_busy():
    manager = DetectorManager([
        {'detector': 1, 'status': 'free'}, 
        {'detector': 2, 'status': 'free'}
    ])
    manager.get_free_detector()
    assert manager.detectors[0]['status'] == 'busy'
    
def test_make_first_busy_use_second_detector():
    manager = DetectorManager([
        {'detector': 1, 'status': 'free'}, 
        {'detector': 2, 'status': 'free'}
    ])
    manager.get_free_detector()
    assert manager.get_free_detector() == 2
    