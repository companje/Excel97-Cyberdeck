class AudioRecorder():

    def __init__(self):
        self._recording = False

    @property
    def is_recording(self):
        return self._recording
    
    def start(self):
        print("start REC")
        self._recording = True

    def stop(self):
        print("stop REC")
        self._recording = False
