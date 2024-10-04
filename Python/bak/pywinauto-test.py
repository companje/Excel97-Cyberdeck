import subprocess
from pywinauto import Application
import time

# Start Excel met verhoogde rechten via runas
subprocess.run(['runas', '/user:Rick', r'"C:\Program Files (x86)\Microsoft Office\Office\EXCEL.EXE"'])

# Wacht een paar seconden totdat Excel volledig is opgestart
time.sleep(5)

# Verbind met het Excel-venster
app = Application().connect(title_re=".*Excel")

# Breng het Excel-venster naar de voorgrond
app.top_window().set_focus()

# Stuur de toetsaanslag 'test'
app.top_window().type_keys('test')
