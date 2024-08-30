import serial
import os
import time
from network_module import *
from scipy.signal import savgol_filter
from collections import deque

window_size = 25
poly_order = 2
data_window = deque(maxlen=window_size)

class SerialReader:
    def __init__(self, port, baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(port, baudrate)
        self.filename = 'is_recording.tmp'
        self.last_message = ''

        self.ser.flush()

    def start_reading(self):
        sensor_index_field = 1
        sensor_index_encoder = 4
        p_encoder_value = -9999
        p_field = ""
        p_num_rows = num_rows = 1

        # try:
        while True:
            while self.ser.in_waiting:
                value = self.ser.readline().decode('utf-8').strip()
                
                self.last_message = value
                
                values = value.split(" ")

                if len(values)!=5:
                    continue

                buttons = values[0]
                
                for i in range(1,7):
                    if str(i) in buttons:
                        num_rows = i
                        break

                if p_num_rows!=num_rows:
                    field_range = ""
                    if num_rows == 6:
                        print("niks wissen")
                        send_udp_message(json.dumps({"action":"select","range":"B28","value":""}), "127.0.0.1", 9999)
                    elif num_rows == 5:
                        field_range = "B28:H28"
                        send_udp_message(json.dumps({"action":"select","range":"B27","value":""}), "127.0.0.1", 9999)
                    elif num_rows == 4:
                        field_range = "B27:H28"
                        send_udp_message(json.dumps({"action":"select","range":"B26","value":""}), "127.0.0.1", 9999)
                    elif num_rows == 3:
                        field_range = "B26:H28"
                        send_udp_message(json.dumps({"action":"select","range":"B25","value":""}), "127.0.0.1", 9999)
                    elif num_rows == 2:
                        field_range = "B25:H28"
                        send_udp_message(json.dumps({"action":"select","range":"B24","value":""}), "127.0.0.1", 9999)
                    elif num_rows == 1:
                        field_range = "B24:H28"
                        send_udp_message(json.dumps({"action":"select","range":"B23","value":""}), "127.0.0.1", 9999)
                    
                    if field_range:
                        send_udp_message(json.dumps({"action":"setValue","range":field_range,"value":""}), "127.0.0.1", 9999)

                    p_num_rows = num_rows
                
                                
                fields = ["B6","B7","B8", "B9", "C13", "C14", "C15", "C16", "C17"]
                for i in range(0,num_rows):
                    fields.append(f"B{23+i}")
                    fields.append(f"H{23+i}")

                field_selector = int(values[sensor_index_field])
                data_window.append(field_selector)
                if len(data_window) < window_size:
                    field_selector = sum(data_window) / len(data_window)
                else:
                    field_selector = savgol_filter(list(data_window), window_length=window_size, polyorder=poly_order)[-1]

                print(field_selector)

                field_selector = 1 - field_selector/1024
                if field_selector>=1:
                    field_selector = .9999            

                field_index = int(field_selector * len(fields))


                field = fields[field_index]

                if field!=p_field:
                    data = {"action":"select","range":field}
                    send_udp_message(json.dumps(data), "127.0.0.1", 9999)
                    p_field = field
                
                encoder_value = int(int(values[sensor_index_encoder]) / 2) # / 2 # because step seems to be always even
                
                if p_encoder_value!=-9999:
                    encoder_delta = encoder_value - p_encoder_value
                else:
                    encoder_delta = 0

                if encoder_delta!=0:
                    # "range":"H23",
                    data = {"action":"increaseValue","value":-encoder_delta}
                    send_udp_message(json.dumps(data), "127.0.0.1", 9999)
                p_encoder_value = encoder_value

                # audio
                if 'T' in value:
                    open(self.filename, 'w').close()  # Create the file
                else:
                    if os.path.exists(self.filename):
                        os.remove(self.filename)  # Delete the file

            time.sleep(.1)  # Prevent high CPU usage
        # except Exception as e:
        #     print(f"Serial reading error: {e}")
        # finally:
        #     self.ser.close()

if __name__ == "__main__":
    serial_reader = SerialReader('COM3', 115200) #'/dev/tty.usbmodem101'
    time.sleep(1)
    serial_reader.start_reading()
