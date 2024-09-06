from network_module import *
#import pyautogui
import time
import keyboard

time.sleep(10)
print("nu")
send_udp_message(json.dumps({"action":"printToPDF"}), "127.0.0.1", 9999)

time.sleep(2)
keyboard.write('test.pdf')
#pyautogui.press('enter')