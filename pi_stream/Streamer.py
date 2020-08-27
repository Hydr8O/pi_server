class Streamer:
    '''Takes frames from the camera and processes them''' 
    def __init__(self, camera):
        self._camera = camera
    
    def stream(self):
        '''Starts to stream video from camera'''
        while True:
            yield self._camera.get_frame()
                    