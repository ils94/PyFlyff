import win32api
import win32con
import time
import random
import globalVariables
import win32gui


def winapi(w, key):
    win32api.SendMessage(w, win32con.WM_KEYDOWN, key, 0)
    time.sleep(random.uniform(0.369420, 0.769420))
    win32api.SendMessage(w, win32con.WM_KEYUP, key, 0)


def send_alt_control_command(igk):
    if globalVariables.alt_control_boolean and igk != "":
        globalVariables.hwndAlt = win32gui.FindWindow(None, "PyFlyff - " + globalVariables.alt_window_name)

        winapi(globalVariables.hwndAlt, igk)
