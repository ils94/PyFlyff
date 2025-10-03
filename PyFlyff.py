import json
import sys
import time

from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PyQt6.QtGui import QKeySequence, QIcon, QShortcut, QAction

from tkinter import Tk, ttk, Frame, Label, Entry, Button, X, W, LEFT, RIGHT, END, OptionMenu, StringVar
from tkinter import messagebox

import random

import globalVariables
import virtualKeys
import profiles
import windowsAPI
import saveConfigJSON
import miscs

import win32gui


class MainWindow(QMainWindow):
    def __init__(self):

        super(MainWindow, self).__init__()

        self.browser = None
        self.setWindowIcon(QIcon(globalVariables.icon))
        self.setMinimumSize(640, 480)
        self.showMaximized()

        self.menu_bar = QMenuBar()
        self.menu_bar.setNativeMenuBar(False)
        self.setMenuBar(self.menu_bar)

        ftool = QAction("Mini FTool", self)
        ftool.triggered.connect(lambda: miscs.multithreading(self.mini_ftool_config))

        alt_control = QAction("Alt Control", self)
        alt_control.triggered.connect(lambda: miscs.multithreading(self.alt_control_config))

        clear_keys = QAction("Reset Hotkeys", self)
        clear_keys.triggered.connect(self.reset_hotkeys)

        menu_tools = self.menu_bar.addMenu("Tools")
        menu_tools.addAction(ftool)
        menu_tools.addAction(alt_control)
        menu_tools.addAction(clear_keys)

        q_action_user_agent = QAction("Set User Agent", self)
        q_action_user_agent.setToolTip("Change your User Agent to something else if you are having trouble "
                                       "connecting your Google Account/Facebook Account/Apple ID, "
                                       "or connecting to the game as a whole.")

        q_action_user_agent.triggered.connect(lambda: miscs.multithreading(miscs.set_user_agent))

        q_action_fullscreen = QAction("Fullscreen | Ctrl+Shift+F11", self)
        q_action_fullscreen.triggered.connect(lambda: miscs.fullscreen(self))

        q_action_open_alt_client = QAction("Open Alt Client | Ctrl+Shift+PageUp", self)
        q_action_open_alt_client.triggered.connect(lambda: self.create_open_client_profile("Alt"))

        q_action_change_main_client_profile = QAction("Change Main Client Profile", self)
        q_action_change_main_client_profile.triggered.connect(lambda: self.create_open_client_profile("Main"))

        self.q_action_always_on_top = QAction("Always on Top: Off", self)
        self.q_action_always_on_top.triggered.connect(lambda: miscs.always_on_top(self))

        menu_client = self.menu_bar.addMenu("Client")
        menu_client.addAction(q_action_user_agent)
        menu_client.addAction(q_action_fullscreen)
        menu_client.addAction(q_action_open_alt_client)
        menu_client.addAction(q_action_change_main_client_profile)
        menu_client.addAction(self.q_action_always_on_top)
        menu_client.setToolTipsVisible(True)

        q_action_flyffipedia = QAction("Flyffipedia", self)
        q_action_flyffipedia.triggered.connect(
            lambda: self.create_new_window("https://flyffipedia.com/", "Flyffipedia"))

        q_action_madrigalinside = QAction("Madrigal Inside", self)
        q_action_madrigalinside.triggered.connect(
            lambda: self.create_new_window("https://madrigalinside.com/", "Madrigal Inside"))

        q_action_flyffulator = QAction("Flyffulator", self)
        q_action_flyffulator.triggered.connect(
            lambda: self.create_new_window("https://flyffulator.com/", "Flyffulator"))

        q_action_madrigalmaps = QAction("Madrigal Maps", self)
        q_action_madrigalmaps.triggered.connect(
            lambda: self.create_new_window("https://www.madrigalmaps.com/", "Madrigal Maps"))

        q_action_flyffmodelviewer = QAction("Flyff Model Viewer", self)
        q_action_flyffmodelviewer.triggered.connect(
            lambda: self.create_new_window("https://flyffmodelviewer.com/", "Flyff Model Viewer"))

        q_action_skillulator = QAction("Skillulator", self)
        q_action_skillulator.triggered.connect(
            lambda: self.create_new_window("https://skillulator.com/", "Skillulator"))

        menu_community = self.menu_bar.addMenu("Community")
        menu_community.addAction(q_action_flyffipedia)
        menu_community.addAction(q_action_madrigalmaps)
        menu_community.addAction(q_action_flyffulator)
        menu_community.addAction(q_action_madrigalmaps)
        menu_community.addAction(q_action_flyffmodelviewer)
        menu_community.addAction(q_action_skillulator)

        self.reload_client = QShortcut(QKeySequence("Ctrl+Shift+F5"), self)
        self.reload_client.activated.connect(lambda: self.reload_main_client())

        self.change_fullscreen = QShortcut(QKeySequence("Ctrl+Shift+F11"), self)
        self.change_fullscreen.activated.connect(lambda: miscs.fullscreen(self))

        self.new_client = QShortcut(QKeySequence("Ctrl+Shift+PgUp"), self)
        self.new_client.activated.connect(lambda: self.create_open_client_profile("Alt"))

        self.mini_ftool_status = self.menu_bar.addMenu("Mini Ftool: OFF")
        self.mini_ftool_status.setDisabled(True)

        self.create_shortcuts()

        self.windows = []

        self.create_open_client_profile("Main")

    def create_new_window(self, link, wn):
        new_window = QWebEngineView()
        new_window.setAttribute(Qt.WA_DeleteOnClose)
        new_window.destroyed.connect(lambda: self.windows.remove(new_window))

        client_folder = "C:/PyFlyff/" + wn.replace(" ", "")

        alt_profile = QWebEngineProfile(wn.replace(" ", ""), new_window)
        alt_profile.setCachePath(client_folder)
        alt_profile.setPersistentStoragePath(client_folder)
        alt_page = QWebEnginePage(alt_profile, new_window)

        new_window.setPage(alt_page)
        new_window.load(QUrl(link))
        new_window.setWindowTitle("PyFlyff - " + wn)
        new_window.setWindowIcon(QIcon(globalVariables.icon))
        new_window.setMinimumSize(640, 480)
        new_window.showMaximized()

        new_window.page().profile().setHttpUserAgent(miscs.load_user_agent(self.windows))

        self.windows.append(new_window)

    def mini_ftool_loop(self):

        counter = 0

        extra_key_time_1 = 0.0
        extra_key_time_2 = 0.0
        extra_key_time_3 = 0.0
        extra_key_time_4 = 0.0

        try:
            while True:

                if counter < globalVariables.mini_ftool_repeat_times and globalVariables.start_mini_ftool_loop is True:

                    windowsAPI.winapi(globalVariables.hwndMain, globals()["mini_ftool_in_game_key_1"])

                    random_wait = random.uniform(globalVariables.mini_ftool_min_interval,
                                                 globals()["mini_ftool_interval_1"])

                    if ("mini_ftool_in_game_key_2" and "mini_ftool_interval_2") in globals():
                        if extra_key_time_1 >= globals()["mini_ftool_interval_2"]:
                            windowsAPI.winapi(globalVariables.hwndMain, globals()["mini_ftool_in_game_key_2"])
                            extra_key_time_1 = 0.0

                    if ("mini_ftool_in_game_key_3" and "mini_ftool_interval_3") in globals():
                        if extra_key_time_2 >= globals()["mini_ftool_interval_3"]:
                            windowsAPI.winapi(globalVariables.hwndMain, globals()["mini_ftool_in_game_key_3"])
                            extra_key_time_2 = 0.0
                            if globalVariables.fix_mini_ftool_loop_var == "YES":
                                extra_key_time_1 = 0.0

                    if ("mini_ftool_in_game_key_4" and "mini_ftool_interval_4") in globals():
                        if extra_key_time_3 >= globals()["mini_ftool_interval_4"]:
                            windowsAPI.winapi(globalVariables.hwndMain, globals()["mini_ftool_in_game_key_4"])
                            extra_key_time_3 = 0.0
                            if globalVariables.fix_mini_ftool_loop_var == "YES":
                                extra_key_time_1 = 0.0
                                extra_key_time_2 = 0.0

                    if ("mini_ftool_in_game_key_5" and "mini_ftool_interval_5") in globals():
                        if extra_key_time_4 >= globals()["mini_ftool_interval_5"]:
                            windowsAPI.winapi(globalVariables.hwndMain, globals()["mini_ftool_in_game_key_5"])
                            extra_key_time_4 = 0.0
                            if globalVariables.fix_mini_ftool_loop_var == "YES":
                                extra_key_time_1 = 0.0
                                extra_key_time_2 = 0.0
                                extra_key_time_3 = 0.0

                    counter += 1

                    time.sleep(random_wait)

                    extra_key_time_1 += random_wait
                    extra_key_time_2 += random_wait
                    extra_key_time_3 += random_wait
                    extra_key_time_4 += random_wait
                else:
                    globalVariables.start_mini_ftool_loop = False
                    self.mini_ftool_status.setTitle("Mini Ftool: OFF")
                    break

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def start_mini_ftool(self):

        globalVariables.hwndMain = win32gui.FindWindow(None, "PyFlyff - " + globalVariables.mini_ftool_window_name)

        self.mini_ftool_status.setTitle("Mini Ftool: ON")

        if not globalVariables.start_mini_ftool_loop:
            if globalVariables.mini_ftool_activation_key != "" and globals()["mini_ftool_in_game_key_1"] != "":
                globalVariables.start_mini_ftool_loop = True
                miscs.multithreading(self.mini_ftool_loop)
        else:
            globalVariables.start_mini_ftool_loop = False

            self.mini_ftool_status.setTitle("Mini Ftool: OFF")

    def mini_ftool_config(self):

        if not globalVariables.menubar_window:

            globalVariables.menubar_window = True

            ftool_config_window = Tk()

            window_width = 300
            window_height = 320

            screen_width = ftool_config_window.winfo_screenwidth()
            screen_height = ftool_config_window.winfo_screenheight()

            x = (screen_width / 2) - (window_width / 2)
            y = (screen_height / 2) - (window_height / 2)

            ftool_config_window.geometry("300x250+" + str(int(x)) + "+" + str(int(y)))
            ftool_config_window.minsize(300, 320)
            ftool_config_window.attributes("-topmost", True)
            ftool_config_window.title("Mini Ftool")
            ftool_config_window.iconbitmap(globalVariables.icon)

            def save():

                for variable in globalVariables.mini_ftool_global_vars:
                    if variable in globals():
                        del globals()[variable]

                globalVariables.mini_ftool_global_vars.clear()

                aux = activation_key_entry.get()

                activation_key_entry.delete(0, END)
                activation_key_entry.insert(0, aux.replace(" ", "").lower())

                aux = in_game_hotkey_entry.get()

                in_game_hotkey_entry.delete(0, END)
                in_game_hotkey_entry.insert(0, aux.replace(" ", "").lower())

                try:

                    list_keys = in_game_hotkey_entry.get().split(",")
                    list_interval = interval_entry.get().split(",")

                    if "" in list_keys:
                        list_keys.remove("")
                    if "" in list_interval:
                        list_interval.remove("")

                    if (activation_key_entry.get()
                        and in_game_hotkey_entry.get()
                        and repeat_times_entry.get()
                        and interval_entry.get()
                        and min_interval_entry.get()
                        and window_combobox.get()) == "":

                        messagebox.showerror("Error", "Fields cannot be empty.")

                    elif any(i for i in list_interval if float(i) < 0):

                        messagebox.showerror("Error", "Intervals cannot be lower than zero.")

                    elif activation_key_entry.get() in list_keys:

                        messagebox.showerror("Error", "Activation Key and In-game Hotkey must be different.")

                    elif activation_key_entry.get() in globalVariables.alt_control_key_list_1:

                        messagebox.showerror("Error", "Main Client HotKey from Alt Control "
                                                      "cannot be the same as the Mini Ftool Activation Key.")
                    elif len(list_keys) != len(list_interval):

                        messagebox.showerror("Error",
                                             "In-Game Hotkey(s) and Interval(s) must have the same "
                                             "amount of values.")
                    elif float(min_interval_entry.get()) > float(list_interval[0]):
                        messagebox.showerror("Error",
                                             "Min Interval cannot be higher than the first Interval.")
                    else:
                        key_counter = 1
                        interval_counter = 1

                        for key in list_keys:
                            globals()["mini_ftool_in_game_key_" + str(key_counter)] = virtualKeys.vk_code.get(key)
                            globalVariables.mini_ftool_global_vars.append("mini_ftool_in_game_key_" + str(key_counter))
                            key_counter += 1
                            if key_counter > len(list_keys):
                                break

                        for interval in list_interval:
                            globals()["mini_ftool_interval_" + str(interval_counter)] = float(interval)
                            globalVariables.mini_ftool_global_vars.append(
                                "mini_ftool_interval_" + str(interval_counter))
                            interval_counter += 1
                            if interval_counter > len(list_interval):
                                break

                        globalVariables.mini_ftool_activation_key = activation_key_entry.get()
                        globalVariables.fix_mini_ftool_loop_var = var.get()
                        globalVariables.mini_ftool_repeat_times = int(repeat_times_entry.get())
                        globalVariables.mini_ftool_window_name = window_combobox.get()
                        globalVariables.mini_ftool_min_interval = float(min_interval_entry.get())

                        self.ftool_key.setKey(globalVariables.mini_ftool_activation_key)

                        saveConfigJSON.save_config_json(file=globalVariables.mini_ftool_json_file, values=(
                            activation_key_entry.get(), in_game_hotkey_entry.get(), repeat_times_entry.get(),
                            interval_entry.get(), min_interval_entry.get(), var.get(), window_combobox.get()))

                        window_combobox["values"] = profiles.save_alt_profiles(window_combobox.get())

                        globalVariables.menubar_window = False
                        ftool_config_window.destroy()

                except Exception as e:
                    messagebox.showerror("Error", str(e))

            profiles.load_alt_profiles()

            explanation_label = Label(ftool_config_window, text="To stop the Mini Ftool, press the activation"
                                                                "\nkey again.", anchor=W, justify="left")
            explanation_label.pack(fill=X, padx=5, pady=5)

            frame = Frame(ftool_config_window)

            frame.pack(fill=X, padx=5, pady=5)

            activation_key_label = Label(frame, text="Activation Key:", width=22, anchor=W)
            activation_key_entry = Entry(frame, width=20)

            in_game_hotkey_label = Label(frame, text="In-Game Hotkey(s):", width=22, anchor=W)
            in_game_hotkey_entry = Entry(frame, width=20)

            repeat_times_label = Label(frame, text="Repeat:", width=22, anchor=W)
            repeat_times_entry = Entry(frame, width=20)

            interval_label = Label(frame, text="Interval(s):", width=22, anchor=W)
            interval_entry = Entry(frame, width=20)

            min_interval_label = Label(frame, text="Min Interval:", width=22, anchor=W)
            min_interval_entry = Entry(frame, width=20)

            fix_mini_ftool_loop_label = Label(frame, text="Fix Loop:", width=22, anchor=W)
            var = StringVar(ftool_config_window)
            var.set("YES")
            fix_mini_ftool_op = OptionMenu(frame, var, "YES", "NO")
            fix_mini_ftool_op.config(width=5)

            window_label = Label(frame, text="Profile Name:", width=22, anchor=W)
            window_combobox = ttk.Combobox(frame, values=globalVariables.profile_list, width=17)

            activation_key_label.grid(row=0, column=0, pady=5)
            activation_key_entry.grid(row=0, column=1, pady=5)

            in_game_hotkey_label.grid(row=1, column=0, pady=5)
            in_game_hotkey_entry.grid(row=1, column=1, pady=5)

            repeat_times_label.grid(row=2, column=0, pady=5)
            repeat_times_entry.grid(row=2, column=1, pady=5)

            interval_label.grid(row=3, column=0, pady=5)
            interval_entry.grid(row=3, column=1, pady=5)

            min_interval_label.grid(row=4, column=0, pady=5)
            min_interval_entry.grid(row=4, column=1, pady=5)

            fix_mini_ftool_loop_label.grid(row=5, column=0, pady=5)
            fix_mini_ftool_op.grid(row=5, column=1, pady=5, sticky=W)

            window_label.grid(row=6, column=0, pady=5)
            window_combobox.grid(row=6, column=1, pady=5)

            button_save = Button(text="Save", width=10, height=1, command=save)
            button_save.pack(padx=5, pady=5)

            try:
                if globalVariables.mini_ftool_json_file_location.exists():
                    with open(globalVariables.mini_ftool_json_file_location) as js:
                        data = json.load(js)

                        activation_key_entry.insert(0, data["activation_key"])
                        in_game_hotkey_entry.insert(0, data["in_game_key"])
                        repeat_times_entry.insert(0, data["repeat_times"])
                        interval_entry.insert(0, data["interval"])
                        min_interval_entry.insert(0, data["min_interval"])
                        var.set(data["fix_loop"])
                        window_combobox.insert(0, data["window"])
            except Exception as e:
                messagebox.showerror("Error", str(e))

            ftool_config_window.wm_protocol("WM_DELETE_WINDOW",
                                            lambda: miscs.destroy_toolbar_windows(ftool_config_window))
            ftool_config_window.mainloop()

    def alt_control_config(self):

        if not globalVariables.menubar_window:

            globalVariables.menubar_window = True

            alt_control_config_window = Tk()

            window_width = 300
            window_height = 280

            screen_width = alt_control_config_window.winfo_screenwidth()
            screen_height = alt_control_config_window.winfo_screenheight()

            x = (screen_width / 2) - (window_width / 2)
            y = (screen_height / 2) - (window_height / 2)

            alt_control_config_window.geometry("300x280+" + str(int(x)) + "+" + str(int(y)))
            alt_control_config_window.minsize(300, 280)
            alt_control_config_window.attributes("-topmost", True)
            alt_control_config_window.title("Alt Control")
            alt_control_config_window.iconbitmap(globalVariables.icon)

            def start():

                self.clear_alt_control_shortcut_keys()

                aux = main_client_hotkey_entry.get()

                main_client_hotkey_entry.delete(0, END)
                main_client_hotkey_entry.insert(0, aux.replace(" ", "").lower())

                aux = alt_client_hotkey_entry.get()

                alt_client_hotkey_entry.delete(0, END)
                alt_client_hotkey_entry.insert(0, aux.replace(" ", "").lower())

                globalVariables.alt_control_key_list_1 = main_client_hotkey_entry.get().split(",")
                globalVariables.alt_control_key_list_2 = alt_client_hotkey_entry.get().split(",")

                try:
                    if (
                            main_client_hotkey_entry.get() and alt_client_hotkey_entry.get() and alt_window_combobox.get()) == "":

                        messagebox.showerror("Error", "Fields cannot be empty.")

                    elif any(e in globalVariables.alt_control_key_list_1 for e in
                             globalVariables.alt_control_key_list_2):

                        messagebox.showerror("Error",
                                             "Main Client Hotkey(s) and Alt Client Hotkey(s) must be different.")

                    elif len(globalVariables.alt_control_key_list_1) != len(globalVariables.alt_control_key_list_2):
                        messagebox.showerror("Error",
                                             "Number of keys must be equal to both Main Client and Alt Client.")

                    elif globalVariables.mini_ftool_activation_key in globalVariables.alt_control_key_list_1:

                        messagebox.showerror("Error", "Main Client HotKey from Alt Control cannot "
                                                      "be the same as the Mini Ftool Activation Key.")

                    else:

                        key1_counter = 1

                        for key1 in globalVariables.alt_control_key_list_1:
                            globals()["acak" + str(key1_counter)] = key1
                            exec('self.alt_control_key_' + str(key1_counter) + '.setKey("' + key1 + '")', None,
                                 locals())
                            key1_counter += 1

                        key2_counter = 1

                        for key2 in globalVariables.alt_control_key_list_2:
                            globals()["acig" + str(key2_counter)] = virtualKeys.vk_code.get(key2)
                            key2_counter += 1

                        globalVariables.alt_window_name = alt_window_combobox.get()

                        saveConfigJSON.save_config_json(file=globalVariables.alt_control_json_file,
                                                        values=(
                                                            main_client_hotkey_entry.get(),
                                                            alt_client_hotkey_entry.get(),
                                                            alt_window_combobox.get()))

                        alt_window_combobox["values"] = profiles.save_alt_profiles(alt_window_combobox.get())

                        globalVariables.alt_control_boolean = True
                        globalVariables.menubar_window = False

                        alt_control_config_window.destroy()

                except Exception as e:
                    messagebox.showerror("Error", str(e))

            def stop():

                self.clear_alt_control_shortcut_keys()

                globalVariables.alt_control_boolean = False

            profiles.load_alt_profiles()

            explanation_label = Label(alt_control_config_window, text="You can assign multiple keys (up to 20 keys)."
                                                                      "\n\nSeparate each key with a comma '','' "
                                                                      "if more than one."
                                                                      "\n\nExample:"
                                                                      "\n\nMain Client Hotkey(s): q,e,f1,f2,v,x..."
                                                                      "\nAlt Client Hotkey(s): 1,2,3,spacebar,z,c...",
                                      anchor=W,
                                      justify="left")
            explanation_label.pack(fill=X, padx=5, pady=5)

            frame = Frame(alt_control_config_window)

            frame.pack(fill=X, padx=5, pady=5)

            main_client_hotkey_label = Label(frame, text="Main Client Hotkey(s):", width=20, anchor=W)
            main_client_hotkey_entry = Entry(frame, width=22)

            alt_client_hotkey_label = Label(frame, text="Alt Client Hotkey(s):", width=20, anchor=W)
            alt_client_hotkey_entry = Entry(frame, width=22)

            alt_window_label = Label(frame, text="Profile Name:", width=20, anchor=W)
            alt_window_combobox = ttk.Combobox(frame, values=globalVariables.profile_list, width=19)

            main_client_hotkey_label.grid(row=0, column=0, pady=5)
            main_client_hotkey_entry.grid(row=0, column=1, pady=5)

            alt_client_hotkey_label.grid(row=1, column=0, pady=5)
            alt_client_hotkey_entry.grid(row=1, column=1, pady=5)

            alt_window_label.grid(row=2, column=0, pady=5)
            alt_window_combobox.grid(row=2, column=1, pady=5)

            button_start = Button(text="Start", width=10, height=1, command=start)
            button_start.pack(side=LEFT, padx=25)

            button_stop = Button(text="Stop", width=10, height=1, command=stop)
            button_stop.pack(side=RIGHT, padx=25)

            try:
                if globalVariables.alt_control_json_file_location.exists():
                    with open(globalVariables.alt_control_json_file_location) as js:
                        data = json.load(js)

                        main_client_hotkey_entry.insert(0, data["activation_key"])
                        alt_client_hotkey_entry.insert(0, data["in_game_key"])
                        alt_window_combobox.insert(0, data["alt_window"])
            except Exception as e:
                messagebox.showerror("Error", str(e))

            alt_control_config_window.wm_protocol("WM_DELETE_WINDOW",
                                                  lambda: miscs.destroy_toolbar_windows(alt_control_config_window))
            alt_control_config_window.mainloop()

    def send_alt_control_command(self, igk):

        if globalVariables.alt_control_boolean and igk != "":
            globalVariables.hwndAlt = win32gui.FindWindow(None, "PyFlyff - " + globalVariables.alt_window_name)

            windowsAPI.winapi(globalVariables.hwndAlt, igk)

    def reset_hotkeys(self):

        if not globalVariables.start_mini_ftool_loop:
            globalVariables.mini_ftool_window_name = ""
            globalVariables.hwndMain = ""
            globalVariables.hwndAlt = ""

            globalVariables.mini_ftool_activation_key = ""
            globalVariables.fix_mini_ftool_loop_var = ""

            for variable in globalVariables.mini_ftool_global_vars:
                if variable in globals():
                    del globals()[variable]

            self.ftool_key.setKey("")

            self.clear_alt_control_shortcut_keys()

    def clear_alt_control_shortcut_keys(self):

        globalVariables.alt_window_name = ""

        key_counter = 1

        for key in globalVariables.alt_control_key_list_1:
            exec('self.alt_control_key_' + str(key_counter) + '.setKey("")', None, locals())
            key_counter += 1

        globalVariables.alt_control_key_list_1.clear()
        globalVariables.alt_control_key_list_2.clear()

    def create_shortcuts(self):

        self.ftool_key = QShortcut(self)
        self.ftool_key.activated.connect(self.start_mini_ftool)

        key_counter = 1

        for key in range(104):
            exec('self.alt_control_key_' + str(key_counter) + ' = QShortcut(self)', globals(), locals())
            exec('self.alt_control_key_' + str(key_counter) +
                 ".activated.connect(lambda: miscs.multithreading("
                 "lambda: windowsAPI.send_alt_control_command(globals()['acig" +
                 str(key_counter) + "'])))", globals(), locals())
            key_counter += 1

    def create_open_client_profile(self, client_type):

        if not globalVariables.menubar_window:

            globalVariables.menubar_window = True

            profile_window = Tk()

            window_width = 300
            window_height = 100

            screen_width = profile_window.winfo_screenwidth()
            screen_height = profile_window.winfo_screenheight()

            x = (screen_width / 2) - (window_width / 2)
            y = (screen_height / 2) - (window_height / 2)

            profile_window.geometry("300x100+" + str(int(x)) + "+" + str(int(y)))
            profile_window.minsize(300, 100)
            profile_window.attributes("-topmost", True)
            profile_window.title("Profile")
            profile_window.iconbitmap(globalVariables.icon)

            def open_profile_new_window():

                try:
                    if profile_window_combobox.get() == "":

                        messagebox.showerror("Error", "Field cannot be empty.")

                    else:

                        profile_window_combobox["values"] = profiles.save_alt_profiles(profile_window_combobox.get())

                        if client_type == "Alt":

                            self.create_new_window(globalVariables.url, profile_window_combobox.get())
                        else:

                            self.browser = None

                            self.browser = QWebEngineView()

                            self.setCentralWidget(self.browser)

                            client_folder = "C:/PyFlyff/" + profile_window_combobox.get().replace(" ", "")

                            main_profile = QWebEngineProfile(profile_window_combobox.get().replace(" ", ""),
                                                             self.browser)
                            main_profile.setCachePath(client_folder)
                            main_profile.setPersistentStoragePath(client_folder)
                            main_page = QWebEnginePage(main_profile, self.browser)

                            self.browser.setPage(main_page)
                            self.browser.setUrl(QUrl(globalVariables.url))
                            self.setWindowTitle("PyFlyff - " + profile_window_combobox.get())

                            self.browser.page().profile().setHttpUserAgent(miscs.load_user_agent(self.windows))

                            globalVariables.can_reload_client = True

                        globalVariables.menubar_window = False
                        profile_window.destroy()

                except Exception as e:
                    messagebox.showerror("Error", str(e))

            profiles.load_alt_profiles()

            profile_window_label = Label(profile_window, text="Create a new profile or choose an existing one.")
            profile_window_combobox = ttk.Combobox(profile_window, values=globalVariables.profile_list)

            profile_window_label.pack(fill=X, pady=5, padx=5)
            profile_window_combobox.pack(fill=X, pady=5, padx=5)

            button_save = Button(text="Open", width=10, height=1, command=open_profile_new_window)
            button_save.pack(pady=5)

            profile_window.wm_protocol("WM_DELETE_WINDOW",
                                       lambda: miscs.destroy_toolbar_windows(profile_window))
            profile_window.mainloop()

    def reload_main_client(self):
        if globalVariables.can_reload_client:
            self.browser.setUrl(QUrl(globalVariables.url))


app = QApplication(sys.argv)

QApplication.setApplicationName("PyFlyff")

window = MainWindow()

app.exec()
