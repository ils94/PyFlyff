import json
import sys
import time

from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QDialog, QLabel, QLineEdit,
                             QComboBox, QGridLayout, QPushButton, QMessageBox, QVBoxLayout,
                             QHBoxLayout)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage
from PyQt6.QtGui import QKeySequence, QIcon, QAction, QShortcut
import random
import global_variables
import virtual_keys
import profiles
import windows_api
import save_config_json
import miscs
import win32gui
from pathlib import Path


class MiniFtoolDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mini Ftool")
        self.setWindowIcon(QIcon(global_variables.icon))
        self.setFixedSize(300, 320)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        layout = QVBoxLayout()

        explanation_label = QLabel("To stop the Mini Ftool, press the activation\nkey again.")
        explanation_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        explanation_label.setWordWrap(True)
        layout.addWidget(explanation_label)

        form_layout = QGridLayout()
        form_layout.setSpacing(5)

        self.activation_key_entry = QLineEdit()
        form_layout.addWidget(QLabel("Activation Key:"), 0, 0)
        form_layout.addWidget(self.activation_key_entry, 0, 1)

        self.in_game_hotkey_entry = QLineEdit()
        form_layout.addWidget(QLabel("In-Game Hotkey(s):"), 1, 0)
        form_layout.addWidget(self.in_game_hotkey_entry, 1, 1)

        self.repeat_times_entry = QLineEdit()
        form_layout.addWidget(QLabel("Repeat:"), 2, 0)
        form_layout.addWidget(self.repeat_times_entry, 2, 1)

        self.interval_entry = QLineEdit()
        form_layout.addWidget(QLabel("Interval(s):"), 3, 0)
        form_layout.addWidget(self.interval_entry, 3, 1)

        self.min_interval_entry = QLineEdit()
        form_layout.addWidget(QLabel("Min Interval:"), 4, 0)
        form_layout.addWidget(self.min_interval_entry, 4, 1)

        self.fix_loop_combo = QComboBox()
        self.fix_loop_combo.addItems(["YES", "NO"])
        form_layout.addWidget(QLabel("Fix Loop:"), 5, 0)
        form_layout.addWidget(self.fix_loop_combo, 5, 1)

        self.window_combobox = QComboBox()
        self.window_combobox.addItems(global_variables.profile_list or [])
        form_layout.addWidget(QLabel("Profile Name:"), 6, 0)
        form_layout.addWidget(self.window_combobox, 6, 1)

        layout.addLayout(form_layout)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)
        layout.addWidget(save_button)

        self.setLayout(layout)

        self.load_config()

    def load_config(self):
        try:
            if global_variables.mini_ftool_json_file_location.exists():
                with open(global_variables.mini_ftool_json_file_location) as js:
                    data = json.load(js)
                    self.activation_key_entry.setText(data["activation_key"])
                    self.in_game_hotkey_entry.setText(data["in_game_key"])
                    self.repeat_times_entry.setText(data["repeat_times"])
                    self.interval_entry.setText(data["interval"])
                    self.min_interval_entry.setText(data["min_interval"])
                    self.fix_loop_combo.setCurrentText(data["fix_loop"])
                    self.window_combobox.setCurrentText(data["window"])
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def save(self):
        for variable in global_variables.mini_ftool_global_vars:
            if variable in globals():
                del globals()[variable]

        global_variables.mini_ftool_global_vars.clear()

        aux = self.activation_key_entry.text()
        self.activation_key_entry.setText(aux.replace(" ", "").lower())

        aux = self.in_game_hotkey_entry.text()
        self.in_game_hotkey_entry.setText(aux.replace(" ", "").lower())

        selected_window = self.window_combobox.currentText()

        try:
            list_keys = [k.strip() for k in self.in_game_hotkey_entry.text().split(",") if k.strip()]
            list_interval = [i.strip() for i in self.interval_entry.text().split(",") if i.strip()]

            if not all([self.activation_key_entry.text(), self.in_game_hotkey_entry.text(),
                        self.repeat_times_entry.text(), self.interval_entry.text(),
                        self.min_interval_entry.text(), selected_window]):
                QMessageBox.critical(self, "Error", "Fields cannot be empty.")
                return

            if list_interval and any(float(i) < 0 for i in list_interval):
                QMessageBox.critical(self, "Error", "Intervals cannot be lower than zero.")
                return

            if self.activation_key_entry.text() in list_keys:
                QMessageBox.critical(self, "Error", "Activation Key and In-game Hotkey must be different.")
                return

            if self.activation_key_entry.text() in global_variables.alt_control_key_list_1:
                QMessageBox.critical(self, "Error", "Main Client HotKey from Alt Control "
                                                    "cannot be the same as the Mini Ftool Activation Key.")
                return

            if len(list_keys) != len(list_interval):
                QMessageBox.critical(self, "Error",
                                     "In-Game Hotkey(s) and Interval(s) must have the same "
                                     "amount of values.")
                return

            if list_interval and float(self.min_interval_entry.text()) > float(list_interval[0]):
                QMessageBox.critical(self, "Error",
                                     "Min Interval cannot be higher than the first Interval.")
                return

            key_counter = 1
            for key in list_keys:
                globals()["mini_ftool_in_game_key_" + str(key_counter)] = virtual_keys.vk_code.get(key)
                global_variables.mini_ftool_global_vars.append("mini_ftool_in_game_key_" + str(key_counter))
                key_counter += 1

            interval_counter = 1
            for interval in list_interval:
                globals()["mini_ftool_interval_" + str(interval_counter)] = float(interval)
                global_variables.mini_ftool_global_vars.append("mini_ftool_interval_" + str(interval_counter))
                interval_counter += 1

            global_variables.mini_ftool_activation_key = self.activation_key_entry.text()
            global_variables.fix_mini_ftool_loop_var = self.fix_loop_combo.currentText()
            global_variables.mini_ftool_repeat_times = int(self.repeat_times_entry.text())
            global_variables.mini_ftool_window_name = selected_window
            global_variables.mini_ftool_min_interval = float(self.min_interval_entry.text())

            self.parent().ftool_key.setKey(QKeySequence(global_variables.mini_ftool_activation_key))

            save_config_json.save_config_json(file=global_variables.mini_ftool_json_file,
                                              values=(self.activation_key_entry.text(),
                                                      self.in_game_hotkey_entry.text(),
                                                      self.repeat_times_entry.text(),
                                                      self.interval_entry.text(),
                                                      self.min_interval_entry.text(),
                                                      self.fix_loop_combo.currentText(),
                                                      selected_window))

            profiles.save_alt_profiles(selected_window)

            global_variables.menubar_window = False
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def closeEvent(self, event):
        miscs.destroy_toolbar_windows(self)
        super().closeEvent(event)


class AltControlDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Alt Control")
        self.setWindowIcon(QIcon(global_variables.icon))
        self.setFixedSize(300, 280)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        layout = QVBoxLayout()

        explanation_label = QLabel("You can assign multiple keys (up to 20 keys).\n\n"
                                   "Separate each key with a comma ',' if more than one.\n\n"
                                   "Example:\n\n"
                                   "Main Client Hotkey(s): q,e,f1,f2,v,x...\n"
                                   "Alt Client Hotkey(s): 1,2,3,spacebar,z,c...")
        explanation_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        explanation_label.setWordWrap(True)
        layout.addWidget(explanation_label)

        form_layout = QGridLayout()
        form_layout.setSpacing(5)

        self.main_client_hotkey_entry = QLineEdit()
        form_layout.addWidget(QLabel("Main Client Hotkey(s):"), 0, 0)
        form_layout.addWidget(self.main_client_hotkey_entry, 0, 1)

        self.alt_client_hotkey_entry = QLineEdit()
        form_layout.addWidget(QLabel("Alt Client Hotkey(s):"), 1, 0)
        form_layout.addWidget(self.alt_client_hotkey_entry, 1, 1)

        self.alt_window_combobox = QComboBox()
        self.alt_window_combobox.addItems(global_variables.profile_list or [])
        form_layout.addWidget(QLabel("Profile Name:"), 2, 0)
        form_layout.addWidget(self.alt_window_combobox, 2, 1)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        start_button = QPushButton("Start")
        start_button.clicked.connect(self.start)
        button_layout.addWidget(start_button)

        stop_button = QPushButton("Stop")
        stop_button.clicked.connect(self.stop)
        button_layout.addWidget(stop_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.load_config()

    def load_config(self):
        try:
            if global_variables.alt_control_json_file_location.exists():
                with open(global_variables.alt_control_json_file_location) as js:
                    data = json.load(js)
                    self.main_client_hotkey_entry.setText(data["activation_key"])
                    self.alt_client_hotkey_entry.setText(data["in_game_key"])
                    self.alt_window_combobox.setCurrentText(data["alt_window"])
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def start(self):
        self.parent().clear_alt_control_shortcut_keys()

        aux = self.main_client_hotkey_entry.text()
        self.main_client_hotkey_entry.setText(aux.replace(" ", "").lower())

        aux = self.alt_client_hotkey_entry.text()
        self.alt_client_hotkey_entry.setText(aux.replace(" ", "").lower())

        selected_window = self.alt_window_combobox.currentText()

        global_variables.alt_control_key_list_1 = [k.strip() for k in self.main_client_hotkey_entry.text().split(",") if
                                                   k.strip()]
        global_variables.alt_control_key_list_2 = [k.strip() for k in self.alt_client_hotkey_entry.text().split(",") if
                                                   k.strip()]

        try:
            if not all([self.main_client_hotkey_entry.text(), self.alt_client_hotkey_entry.text(), selected_window]):
                QMessageBox.critical(self, "Error", "Fields cannot be empty.")
                return

            if any(e in global_variables.alt_control_key_list_1 for e in global_variables.alt_control_key_list_2):
                QMessageBox.critical(self, "Error",
                                     "Main Client Hotkey(s) and Alt Client Hotkey(s) must be different.")
                return

            if len(global_variables.alt_control_key_list_1) != len(global_variables.alt_control_key_list_2):
                QMessageBox.critical(self, "Error",
                                     "Number of keys must be equal to both Main Client and Alt Client.")
                return

            if global_variables.mini_ftool_activation_key in global_variables.alt_control_key_list_1:
                QMessageBox.critical(self, "Error", "Main Client HotKey from Alt Control cannot "
                                                    "be the same as the Mini Ftool Activation Key.")
                return

            key1_counter = 1
            for key1 in global_variables.alt_control_key_list_1:
                globals()["acak" + str(key1_counter)] = key1
                if key1_counter in self.parent().alt_control_shortcuts:
                    self.parent().alt_control_shortcuts[key1_counter].setKey(QKeySequence(key1))
                key1_counter += 1

            key2_counter = 1
            for key2 in global_variables.alt_control_key_list_2:
                globals()["acig" + str(key2_counter)] = virtual_keys.vk_code.get(key2)
                key2_counter += 1

            global_variables.alt_window_name = selected_window

            save_config_json.save_config_json(file=global_variables.alt_control_json_file,
                                              values=(self.main_client_hotkey_entry.text(),
                                                      self.alt_client_hotkey_entry.text(),
                                                      selected_window))

            profiles.save_alt_profiles(selected_window)

            global_variables.alt_control_boolean = True
            global_variables.menubar_window = False
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def stop(self):
        self.parent().clear_alt_control_shortcut_keys()
        global_variables.alt_control_boolean = False

    def closeEvent(self, event):
        miscs.destroy_toolbar_windows(self)
        super().closeEvent(event)


class ProfileDialog(QDialog):
    def __init__(self, parent=None, client_type="Main"):
        super().__init__(parent)
        self.client_type = client_type
        self.setWindowTitle("Profile")
        self.setWindowIcon(QIcon(global_variables.icon))
        self.setFixedSize(300, 100)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        layout = QVBoxLayout()

        label = QLabel("Create a new profile or choose an existing one.")
        layout.addWidget(label)

        self.profile_combobox = QComboBox()
        self.profile_combobox.setEditable(True)
        self.profile_combobox.addItems(global_variables.profile_list or [])
        layout.addWidget(self.profile_combobox)

        open_button = QPushButton("Open")
        open_button.clicked.connect(self.open_profile)
        layout.addWidget(open_button)

        self.setLayout(layout)

    def open_profile(self):
        try:
            selected = self.profile_combobox.currentText()
            if not selected:
                QMessageBox.critical(self, "Error", "Field cannot be empty.")
                return

            profiles.save_alt_profiles(selected)

            if self.client_type == "Alt":
                self.parent().create_new_window(global_variables.url, selected)
            else:
                self.parent().browser = None
                self.parent().browser = QWebEngineView()
                self.parent().setCentralWidget(self.parent().browser)

                client_folder = Path(global_variables.data_folder) / selected.replace(" ", "")

                main_profile = QWebEngineProfile(selected.replace(" ", ""),
                                                 self.parent().browser)
                main_profile.setCachePath(str(client_folder))
                main_profile.setPersistentStoragePath(str(client_folder))
                main_page = QWebEnginePage(main_profile, self.parent().browser)

                self.parent().browser.setPage(main_page)
                self.parent().browser.setUrl(QUrl(global_variables.url))
                self.parent().setWindowTitle("PyFlyff - " + selected)

                self.parent().browser.page().profile().setHttpUserAgent(
                    miscs.load_user_agent(self.parent().windows))

                global_variables.can_reload_client = True

            global_variables.menubar_window = False
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def closeEvent(self, event):
        miscs.destroy_toolbar_windows(self)
        super().closeEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):

        super(MainWindow, self).__init__()

        self.browser = None
        self.setWindowIcon(QIcon(global_variables.icon))
        self.setMinimumSize(640, 480)
        self.showMaximized()

        self.menu_bar = QMenuBar()
        self.menu_bar.setNativeMenuBar(False)
        self.setMenuBar(self.menu_bar)

        ftool = QAction("Mini FTool", self)
        ftool.triggered.connect(self.mini_ftool_config)

        alt_control = QAction("Alt Control", self)
        alt_control.triggered.connect(self.alt_control_config)

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

        q_action_user_agent.triggered.connect(miscs.set_user_agent)

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
        menu_community.addAction(q_action_madrigalinside)
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
        new_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        new_window.destroyed.connect(lambda: self.windows.remove(new_window))

        client_folder = Path(global_variables.data_folder) / wn.replace(" ", "")

        alt_profile = QWebEngineProfile(wn.replace(" ", ""), new_window)
        alt_profile.setCachePath(str(client_folder))
        alt_profile.setPersistentStoragePath(str(client_folder))
        alt_page = QWebEnginePage(alt_profile, new_window)

        new_window.setPage(alt_page)
        new_window.load(QUrl(link))
        new_window.setWindowTitle("PyFlyff - " + wn)
        new_window.setWindowIcon(QIcon(global_variables.icon))
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

                if counter < global_variables.mini_ftool_repeat_times and global_variables.start_mini_ftool_loop is True:

                    windows_api.winapi(global_variables.hwndMain, globals()["mini_ftool_in_game_key_1"])

                    random_wait = random.uniform(global_variables.mini_ftool_min_interval,
                                                 globals()["mini_ftool_interval_1"])

                    if "mini_ftool_in_game_key_2" in globals() and "mini_ftool_interval_2" in globals():
                        if extra_key_time_1 >= globals()["mini_ftool_interval_2"]:
                            windows_api.winapi(global_variables.hwndMain, globals()["mini_ftool_in_game_key_2"])
                            extra_key_time_1 = 0.0

                    if "mini_ftool_in_game_key_3" in globals() and "mini_ftool_interval_3" in globals():
                        if extra_key_time_2 >= globals()["mini_ftool_interval_3"]:
                            windows_api.winapi(global_variables.hwndMain, globals()["mini_ftool_in_game_key_3"])
                            extra_key_time_2 = 0.0
                            if global_variables.fix_mini_ftool_loop_var == "YES":
                                extra_key_time_1 = 0.0

                    if "mini_ftool_in_game_key_4" in globals() and "mini_ftool_interval_4" in globals():
                        if extra_key_time_3 >= globals()["mini_ftool_interval_4"]:
                            windows_api.winapi(global_variables.hwndMain, globals()["mini_ftool_in_game_key_4"])
                            extra_key_time_3 = 0.0
                            if global_variables.fix_mini_ftool_loop_var == "YES":
                                extra_key_time_1 = 0.0
                                extra_key_time_2 = 0.0

                    if "mini_ftool_in_game_key_5" in globals() and "mini_ftool_interval_5" in globals():
                        if extra_key_time_4 >= globals()["mini_ftool_interval_5"]:
                            windows_api.winapi(global_variables.hwndMain, globals()["mini_ftool_in_game_key_5"])
                            extra_key_time_4 = 0.0
                            if global_variables.fix_mini_ftool_loop_var == "YES":
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
                    global_variables.start_mini_ftool_loop = False
                    self.mini_ftool_status.setTitle("Mini Ftool: OFF")
                    break

        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))

    def start_mini_ftool(self):

        global_variables.hwndMain = win32gui.FindWindow(None, "PyFlyff - " + global_variables.mini_ftool_window_name)

        self.mini_ftool_status.setTitle("Mini Ftool: ON")

        if not global_variables.start_mini_ftool_loop:
            if global_variables.mini_ftool_activation_key != "" and "mini_ftool_in_game_key_1" in globals() and \
                    globals()["mini_ftool_in_game_key_1"] != "":
                global_variables.start_mini_ftool_loop = True
                miscs.multithreading(self.mini_ftool_loop)
        else:
            global_variables.start_mini_ftool_loop = False

            self.mini_ftool_status.setTitle("Mini Ftool: OFF")

    def mini_ftool_config(self):

        if not global_variables.menubar_window:
            global_variables.menubar_window = True
            profiles.load_alt_profiles()
            dialog = MiniFtoolDialog(self)
            dialog.exec()

    def alt_control_config(self):

        if not global_variables.menubar_window:
            global_variables.menubar_window = True
            profiles.load_alt_profiles()
            dialog = AltControlDialog(self)
            dialog.exec()

    def send_alt_control_command(self, igk):

        if global_variables.alt_control_boolean and igk != "":
            try:
                global_variables.hwndAlt = win32gui.FindWindow(None, "PyFlyff - " + global_variables.alt_window_name)
                if global_variables.hwndAlt:
                    windows_api.winapi(global_variables.hwndAlt, igk)
                else:
                    print("Alt window not found")
            except Exception as e:
                print(f"Error sending key: {e}")
                QMessageBox.critical(None, "Error", str(e))

    def _trigger_alt_key(self, idx):
        igk = globals().get(f"acig{idx}", 0)
        if igk:
            miscs.multithreading(lambda: self.send_alt_control_command(igk))

    def reset_hotkeys(self):

        if not global_variables.start_mini_ftool_loop:
            global_variables.mini_ftool_window_name = ""
            global_variables.hwndMain = ""
            global_variables.hwndAlt = ""

            global_variables.mini_ftool_activation_key = ""
            global_variables.fix_mini_ftool_loop_var = ""

            for variable in global_variables.mini_ftool_global_vars:
                if variable in globals():
                    del globals()[variable]

            self.ftool_key.setKey(QKeySequence(""))

            self.clear_alt_control_shortcut_keys()

    def clear_alt_control_shortcut_keys(self):

        global_variables.alt_window_name = ""

        for shortcut in self.alt_control_shortcuts.values():
            shortcut.setKey(QKeySequence(""))

        global_variables.alt_control_key_list_1.clear()
        global_variables.alt_control_key_list_2.clear()

    def create_shortcuts(self):

        self.ftool_key = QShortcut(self)
        self.ftool_key.activated.connect(self.start_mini_ftool)

        self.alt_control_shortcuts = {}
        for i in range(1, 21):
            shortcut = QShortcut(self)
            shortcut.activated.connect(lambda idx=i: self._trigger_alt_key(idx))
            self.alt_control_shortcuts[i] = shortcut

    def create_open_client_profile(self, client_type):

        if not global_variables.menubar_window:
            global_variables.menubar_window = True
            profiles.load_alt_profiles()
            dialog = ProfileDialog(self, client_type)
            dialog.exec()

    def reload_main_client(self):
        if global_variables.can_reload_client:
            self.browser.setUrl(QUrl(global_variables.url))


app = QApplication(sys.argv)

QApplication.setApplicationName("PyFlyff")

window = MainWindow()

app.exec()
