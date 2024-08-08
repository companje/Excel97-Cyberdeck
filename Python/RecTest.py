import sounddevice as sd
import soundfile as sf
import serial
import threading

class AudioRecorder:
    def __init__(self, filename="output.wav", samplerate=44100, channels=1):
        self.filename = filename
        self.samplerate = samplerate
        self.channels = channels
        self.frames = []
        self.recording = False

    def start_recording(self):
        self.recording = True
        threading.Thread(target=self._record).start()

    def _record(self):
        with sf.SoundFile(self.filename, mode='w', samplerate=self.samplerate, channels=self.channels) as file:
            with sd.InputStream(samplerate=self.samplerate, channels=self.channels, callback=self.callback):
                while self.recording:
                    sd.sleep(100)

    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.frames.append(indata.copy())

    def stop_recording(self):
        self.recording = False
        # Save frames to file
        with sf.SoundFile(self.filename, mode='w', samplerate=self.samplerate, channels=self.channels) as file:
            for frame in self.frames:
                file.write(frame)

class SerialReader:
    def __init__(self, port, baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(port, baudrate)
        self.reading = False

    def start_reading(self, audio_recorder):
        self.reading = True
        threading.Thread(target=self._read, args=(audio_recorder,)).start()

    def _read(self, audio_recorder):
        while self.reading:
            # if self.ser.in_waiting:
                value = self.ser.readline().decode('utf-8').strip()

                print(value)

                if len(value)>15:
                    value = value[15]

                if value == 'T':
                    print("recv T")
                    if not audio_recorder.recording:
                        audio_recorder.start_recording()
                else:
                    if audio_recorder.recording:
                        audio_recorder.stop_recording()

    def stop_reading(self):
        self.reading = False
        self.ser.close()

if __name__ == "__main__":
    audio_recorder = AudioRecorder()
    serial_reader = SerialReader('COM3')  # Pas aan naar de juiste seriële poort
    serial_reader.start_reading(audio_recorder)
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        serial_reader.stop_reading()
        if audio_recorder.recording:
            audio_recorder.stop_recording()


