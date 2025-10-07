import win32api
import win32con
import time
import random
import global_variables
import win32gui


def winapi(w, key):
    win32api.SendMessage(w, win32con.WM_KEYDOWN, key, 0)
    time.sleep(random.uniform(0.369420, 0.769420))
    win32api.SendMessage(w, win32con.WM_KEYUP, key, 0)


def send_alt_control_command(igk):
    if global_variables.alt_control_boolean and igk != "":
        global_variables.hwndAlt = win32gui.FindWindow(None, "PyFlyff - " + global_variables.alt_window_name)

        winapi(global_variables.hwndAlt, igk)
