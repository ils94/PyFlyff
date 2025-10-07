from tkinter import Tk, messagebox, Label, Entry, Button, X

from PyQt6.QtWidgets import QErrorMessage
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import json
import global_variables
import save_config_json
import threading


def destroy_toolbar_windows(w):
    global_variables.menubar_window = False
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
    if not global_variables.menubar_window:

        global_variables.menubar_window = True

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
        user_agent_config_window.iconbitmap(global_variables.icon)

        def save():

            try:
                if user_agent_entry.get() == "":

                    messagebox.showerror("Error", "Field cannot be empty.")

                else:

                    save_config_json.save_config_json(file=global_variables.user_agent_json_file,
                                                      values=(user_agent_entry.get(),))

                    global_variables.menubar_window = False
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

        if global_variables.user_agent == "":
            user_agent_entry.insert(0, global_variables.default_user_agent)
        else:
            user_agent_entry.insert(0, global_variables.user_agent)

        user_agent_config_window.wm_protocol("WM_DELETE_WINDOW",
                                             lambda: destroy_toolbar_windows(user_agent_config_window))

        user_agent_config_window.mainloop()


def load_user_agent(w):
    try:
        if global_variables.user_agent_json_file_location.exists():
            with open(global_variables.user_agent_json_file_location) as js:
                data = json.load(js)
                global_variables.user_agent = data["user_agent"]

        if global_variables.user_agent == "":
            return global_variables.default_user_agent
        else:
            return global_variables.user_agent
    except KeyError as e:
        error_dialog = QErrorMessage()
        error_dialog.showMessage("Key not found in UserAgent.json: " + str(e) + "\nMake sure the key is valid "
                                                                                "inside the file, or delete "
                                                                                "the file "
                                                                                "''C:/PyFlyff/UserAgent.json'' "
                                                                                "to create a new one by setting "
                                                                                "a new User Agent.")
        error_dialog.setWindowIcon(QIcon(global_variables.icon))
        w.append(error_dialog)


def always_on_top(w):
    if not global_variables.is_on_top:
        # Turn on: Add the flag to existing ones
        w.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        w.q_action_always_on_top.setText("Always on Top: On")
        global_variables.is_on_top = True
    else:
        # Turn off: Remove only the flag from existing ones
        w.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
        w.q_action_always_on_top.setText("Always on Top: Off")
        global_variables.is_on_top = False
    w.show()  # Apply changes
