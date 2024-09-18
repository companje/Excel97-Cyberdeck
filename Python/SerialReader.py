import serial
import os
import time
from network_module import *
#from scipy.signal import savgol_filter
from collections import deque
import pygetwindow as gw
from datetime import datetime
import pyautogui


class SerialReader:
    def __init__(self, port, baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(port, baudrate)
        self.filename = 'is_recording.tmp'
        self.use_gpt_filename = 'use_gpt.tmp'
        self.last_message = ''
        self.prev_print_time = 0

        # self.ser.flush()

        while self.ser.in_waiting: # extra flush
            print("extra flush")
            value = self.ser.readline()            


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
                
                # print(value)

                self.last_message = value
                
                values = value.split(" ")

                if len(values)!=6:
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
                
                field_index = int(values[5])//2 % len(fields)
                
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

                # use gpt
                if 'L' in value:
                    open(self.use_gpt_filename, 'w').close()  # Create the file
                else:
                    if os.path.exists(self.use_gpt_filename):
                        os.remove(self.use_gpt_filename)  # Delete the file


                if 'P' in value and time.time()-self.prev_print_time>5: # debounce 5 sec 
                    print("PRINT")
                    self.prev_print_time = time.time()
                    window = gw.getWindowsWithTitle('Microsoft Excel - cyberdeck.xls')[0]
                    filename = datetime.now().strftime("%Y-%m-%d-%H.%M.pdf")
                    send_udp_message(json.dumps( {"action":"printToPDF", "value": filename}), "127.0.0.1", 9999)

                    if window:
                        window.activate()

                    time.sleep(.1)
                    pyautogui.write("D:\\")
                    pyautogui.press('enter')
                    time.sleep(.3)
                    pyautogui.write(filename)
                    time.sleep(.3)
                    pyautogui.press('enter')


            time.sleep(.1)  # Prevent high CPU usage
        # except Exception as e:
        #     print(f"Serial reading error: {e}")
        # finally:
        #     self.ser.close()

if __name__ == "__main__":
    serial_reader = SerialReader('COM3', 115200) #'/dev/tty.usbmodem101'
    time.sleep(1)
    serial_reader.start_reading()
