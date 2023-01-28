import win32api, win32con
from win32gui import GetWindowText, GetForegroundWindow

class Keyboard:
    def __init__(self, window_name : str) -> None:
        self.window_name = window_name

    def keydown(self, keycode : str, background=False):
        
        pressed = win32api.GetAsyncKeyState(ord(keycode.capitalize())) & 1
        
        if pressed and GetWindowText(GetForegroundWindow()) == self.window_name and not background:
            return True
        elif pressed and background:
            return True
        else:
            return False