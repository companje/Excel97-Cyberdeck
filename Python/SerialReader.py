import serial
import threading
import time

class SerialReader:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port, baudrate)
        self.is_talking = False
        self.running = False
        self.thread = threading.Thread(target=self._background_task)

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def _background_task(self):
        while self.running:
            self.update()
            time.sleep(0.1)  # Even pauzeren om CPU-gebruik te minimaliseren

    def update(self):
        try:
            line = self.ser.readline().decode('utf-8').strip()
            if len(line)<24:
                return
            
            self.is_talking = line[15] != "."
        except Exception as e:
            print(f"Error reading line: {e}")
            return
        
        
