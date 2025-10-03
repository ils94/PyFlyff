from tkinter import Tk, messagebox, Label, Entry, Button, X

from PyQt6.QtWidgets import QErrorMessage
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import json
import globalVariables
import saveConfigJSON
import threading


def destroy_toolbar_windows(w):
    globalVariables.menubar_window = False
    w.destroy()


def multithreading(function):
    threading.Thread(target=function).start()


def fullscreen(w):
    if w.isFullScreen():
        w.showMaximized()
        w.menu_bar.setVisible(True)
    else:
        w.showFullScreen()
        w.menu_bar.setVisible(False)


def set_user_agent():
    if not globalVariables.menubar_window:

        globalVariables.menubar_window = True

        user_agent_config_window = Tk()

        window_width = 300
        window_height = 130

        screen_width = user_agent_config_window.winfo_screenwidth()
        screen_height = user_agent_config_window.winfo_screenheight()

        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)

        user_agent_config_window.geometry("300x130+" + str(int(x)) + "+" + str(int(y)))
        user_agent_config_window.minsize(300, 130)
        user_agent_config_window.attributes("-topmost", True)
        user_agent_config_window.title("User Agent")
        user_agent_config_window.iconbitmap(globalVariables.icon)

        def save():

            try:
                if user_agent_entry.get() == "":

                    messagebox.showerror("Error", "Field cannot be empty.")

                else:

                    saveConfigJSON.save_config_json(file=globalVariables.user_agent_json_file,
                                                    values=(user_agent_entry.get(),))

                    globalVariables.menubar_window = False
                    user_agent_config_window.destroy()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        user_agent_label = Label(user_agent_config_window, text="Set your User Agent below:")
        user_agent_entry = Entry(user_agent_config_window)
        restart_label = Label(user_agent_config_window, text="After setting your User Agent, restart the Client.")

        user_agent_label.pack(fill=X, pady=5, padx=5)
        user_agent_entry.pack(fill=X, pady=5, padx=5)
        restart_label.pack(fill=X, pady=5, padx=5)

        button_save = Button(text="Save", width=10, height=1, command=save)
        button_save.pack(pady=5)

        if globalVariables.user_agent == "":
            user_agent_entry.insert(0, globalVariables.default_user_agent)
        else:
            user_agent_entry.insert(0, globalVariables.user_agent)

        user_agent_config_window.wm_protocol("WM_DELETE_WINDOW",
                                             lambda: destroy_toolbar_windows(user_agent_config_window))

        user_agent_config_window.mainloop()


def load_user_agent(w):
    try:
        if globalVariables.user_agent_json_file_location.exists():
            with open(globalVariables.user_agent_json_file_location) as js:
                data = json.load(js)
                globalVariables.user_agent = data["user_agent"]

        if globalVariables.user_agent == "":
            return globalVariables.default_user_agent
        else:
            return globalVariables.user_agent
    except KeyError as e:
        error_dialog = QErrorMessage()
        error_dialog.showMessage("Key not found in UserAgent.json: " + str(e) + "\nMake sure the key is valid "
                                                                                "inside the file, or delete "
                                                                                "the file "
                                                                                "''C:/PyFlyff/UserAgent.json'' "
                                                                                "to create a new one by setting "
                                                                                "a new User Agent.")
        error_dialog.setWindowIcon(QIcon(globalVariables.icon))
        w.append(error_dialog)


def always_on_top(w):
    if not globalVariables.is_on_top:
        w.setWindowFlag(Qt.WindowStaysOnTopHint)
        w.show()
        w.q_action_always_on_top.setText("Always on Top: On")
        globalVariables.is_on_top = True
    else:
        w.setWindowFlags(
            Qt.Window |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint |
            Qt.WindowMinimizeButtonHint |
            Qt.WindowMaximizeButtonHint)
        w.show()
        w.q_action_always_on_top.setText("Always on Top: Off")
        globalVariables.is_on_top = False
