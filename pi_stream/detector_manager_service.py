class DetectorManager:
    '''Decides which detector should be used for a client'''
    def __init__(self, detectors):
        self._detectors = detectors
        self._current_detector_index = 0
        #[{'detector': detector, 'status': 'free'}]
    def get_current_detector(self):
        for detector in self._detectors:
            if detector['status'] == 'free':
                detector['status'] == 'busy'
                return detector
            