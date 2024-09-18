from network_module import *
import pyautogui
import time
# import keyboard
import pygetwindow as gw
from datetime import datetime

time.sleep(1)
print("nu")

window = gw.getWindowsWithTitle('Microsoft Excel - cyberdeck.xls')[0]

filename = datetime.now().strftime("%Y-%m-%d-%H.%M.pdf")

send_udp_message(json.dumps( {"action":"printToPDF", "value": filename}), "127.0.0.1", 9999)

if window:
    window.activate()

time.sleep(.1)
pyautogui.write("D:")
pyautogui.press('enter')
time.sleep(.3)
pyautogui.write(filename)
time.sleep(.3)
pyautogui.press('enter')
