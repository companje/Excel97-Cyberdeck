import serial
import os
import time
from network_module import *



class SerialReader:
    def __init__(self, port, baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(port, baudrate)
        self.filename = 'is_recording.tmp'
        self.last_message = ''

    def start_reading(self):
        p_encoder_value = -1

        try:
            while True:
                while self.ser.in_waiting:
                    value = self.ser.readline().decode('utf-8').strip()
                    
                    self.last_message = value
                    
                    values = value.split(" ")

                    encoder_value = values[-1]
                    if encoder_value!=p_encoder_value:
                        data = {"action":"setValue","range":"H23","value":encoder_value}
                        send_udp_message(json.dumps(data), "127.0.0.1", 9999)
                    p_encoder_value = encoder_value

                    # audio
                    if 'T' in value:
                        open(self.filename, 'w').close()  # Create the file
                    else:
                        if os.path.exists(self.filename):
                            os.remove(self.filename)  # Delete the file

                time.sleep(.1)  # Prevent high CPU usage
        except Exception as e:
            print(f"Serial reading error: {e}")
        finally:
            self.ser.close()

if __name__ == "__main__":
    serial_reader = SerialReader('COM3', 115200) #'/dev/tty.usbmodem101'
    time.sleep(1)
    serial_reader.start_reading()
