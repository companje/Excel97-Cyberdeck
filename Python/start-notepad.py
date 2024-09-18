import subprocess
import pyautogui
import time

# Start Notepad
subprocess.Popen(['notepad.exe'])

# Wacht even zodat Notepad kan opstarten
time.sleep(2)

# Typ het woord 'test'
pyautogui.write('test')
