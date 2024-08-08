import sounddevice as sd
import soundfile as sf
import serial
import threading
import queue

class AudioRecorder:
    def __init__(self, filename="output.wav", samplerate=44100, channels=1):
        self.filename = filename
        self.samplerate = samplerate
        self.channels = channels
        self.q = queue.Queue()
        self.recording = threading.Event()
        self.thread = None

    def start_recording(self):
        print("start")
        self.recording.set()
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def _record(self):
        try:
            with sf.SoundFile(self.filename, mode='w', samplerate=self.samplerate, channels=self.channels) as file:
                with sd.InputStream(samplerate=self.samplerate, channels=self.channels, callback=self.callback):
                    while self.recording.is_set():
                        while not self.q.empty():
                            file.write(self.q.get())
                        sd.sleep(100)
        except Exception as e:
            print(f"Recording error: {e}")

    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.q.put(indata.copy())

    def stop_recording(self):
        print("stop")
        self.recording.clear()
        if self.thread:
            self.thread.join()
        with sf.SoundFile(self.filename, mode='w', samplerate=self.samplerate, channels=self.channels) as file:
            while not self.q.empty():
                file.write(self.q.get())

class SerialReader:
    def __init__(self, port, baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(port, baudrate)
        self.reading = threading.Event()

    def start_reading(self, audio_recorder):
        self.reading.set()
        threading.Thread(target=self._read, args=(audio_recorder,)).start()

    def _read(self, audio_recorder):
        try:
            while self.reading.is_set():
                if self.ser.in_waiting:
                    value = self.ser.readline().decode('utf-8').strip()
                    print(value)

                    if len(value) > 15:
                        value = value[15]

                    if value == 'T':
                        if not audio_recorder.recording.is_set():
                            audio_recorder.start_recording()
                    else:
                        if audio_recorder.recording.is_set():
                            audio_recorder.stop_recording()
        except Exception as e:
            print(f"Serial reading error: {e}")

    def stop_reading(self):
        self.reading.clear()
        self.ser.close()

if __name__ == "__main__":
    audio_recorder = AudioRecorder()
    serial_reader = SerialReader('/dev/tty.usbmodem101', 9600)
    serial_reader.start_reading(audio_recorder)

    try:
        while True:
            print("waiting")
            sd.sleep(100)
    except KeyboardInterrupt:
        serial_reader.stop_reading()
        if audio_recorder.recording.is_set():
            audio_recorder.stop_recording()
