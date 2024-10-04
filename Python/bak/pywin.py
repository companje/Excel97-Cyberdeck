import subprocess
import pyautogui
import time
import pygetwindow as gw

# for t in gw.getAllTitles():
#     print(t)


# # Start Notepad
# subprocess.Popen(['notepad.exe'])

# # Wacht even zodat Notepad kan opstarten
time.sleep(5)

# # Haal het Notepad-venster op (aangenomen dat de titel 'Untitled - Notepad' is)
window = gw.getWindowsWithTitle('Microsoft Excel - cyberdeck.xls')[0]
print(window)
# # # Breng het Notepad-venster naar de voorgrond
if window:
    window.activate()

# # Typ het woord 'test'
pyautogui.write('test')
