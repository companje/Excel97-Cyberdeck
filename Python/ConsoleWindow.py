import ctypes

# Handle to the console window
hwnd = ctypes.windll.kernel32.GetConsoleWindow()

# Structuur voor het opslaan van positie en grootte
class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long)
    ]

# Functie om het venster te verplaatsen
def move_console_window(x, y):
    rect = RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
    width = rect.right - rect.left
    height = rect.bottom - rect.top
    ctypes.windll.user32.MoveWindow(hwnd, x, y, width, height, True)

