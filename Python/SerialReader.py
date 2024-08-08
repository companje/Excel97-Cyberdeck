import serial
import os
import time

class SerialReader:
    def __init__(self, port, baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(port, baudrate)
        self.filename = 'is_recording.tmp'
        self.last_message = ''

    def start_reading(self):
        try:
            while True:
                while self.ser.in_waiting:
                    value = self.ser.readline().decode('utf-8').strip()
                    
                    self.last_message = value
                    
                    print(value)

                    if 'T' in value:
                        open(self.filename, 'w').close()  # Create the file
                    else:
                        if os.path.exists(self.filename):
                            os.remove(self.filename)  # Delete the file

                time.sleep(0.1)  # Prevent high CPU usage
        except Exception as e:
            print(f"Serial reading error: {e}")
        finally:
            self.ser.close()

if __name__ == "__main__":
    serial_reader = SerialReader('/dev/tty.usbmodem101', 9600)
    serial_reader.start_reading()
