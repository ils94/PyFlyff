import json
import threading
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox, QErrorMessage
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

import global_variables
import save_config_json


def destroy_toolbar_windows(window: QWidget):
    global_variables.menubar_window = False
    window.close()


def multithreading(function):
    threading.Thread(target=function, daemon=True).start()


def fullscreen(window: QWidget):
    if window.isFullScreen():
        window.showMaximized()
        window.menu_bar.setVisible(True)
    else:
        window.showFullScreen()
        window.menu_bar.setVisible(False)


def set_user_agent():
    if global_variables.menubar_window:
        return  # Evita abrir múltiplas vezes

    global_variables.menubar_window = True

    window = QWidget()
    window.setWindowTitle("User Agent")
    window.setWindowIcon(QIcon(global_variables.icon))
    window.setFixedSize(420, 190)
    window.setWindowFlags(window.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

    # Centraliza na tela
    screen = QApplication.primaryScreen().availableGeometry()
    window.move(
        (screen.width() - window.width()) // 2,
        (screen.height() - window.height()) // 2
    )

    layout = QVBoxLayout(window)

    lbl_title = QLabel("Set your User Agent below:")
    lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(lbl_title)

    entry = QLineEdit()
    entry.setText(global_variables.user_agent or global_variables.default_user_agent)
    layout.addWidget(entry)

    lbl_restart = QLabel("After setting your User Agent, restart the Client.")
    lbl_restart.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lbl_restart.setWordWrap(True)
    layout.addWidget(lbl_restart)

    def save():
        ua = entry.text().strip()
        if not ua:
            QMessageBox.critical(window, "Error", "Field cannot be empty.")
            return

        try:
            save_config_json.save_config_json(
                file=global_variables.user_agent_json_file,
                values=(ua,)
            )
            global_variables.user_agent = ua
            destroy_toolbar_windows(window)
        except Exception as e:
            QMessageBox.critical(window, "Error", str(e))

    btn = QPushButton("Save")
    btn.setFixedHeight(40)
    btn.clicked.connect(save)
    layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

    # Fechar com X do Windows
    def close_event(event):
        destroy_toolbar_windows(window)
        event.accept()

    window.closeEvent = close_event

    window.show()


def load_user_agent(main_window):
    try:
        file_path = global_variables.user_agent_json_file_location
        if Path(file_path).exists():
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                global_variables.user_agent = data["user_agent"]

        if not global_variables.user_agent:
            return global_variables.default_user_agent
        else:
            return global_variables.user_agent

    except KeyError as e:
        error_dialog = QErrorMessage(main_window)
        error_dialog.setWindowTitle("User Agent Error")
        error_dialog.setWindowIcon(QIcon(global_variables.icon))
        error_dialog.showMessage(
            f"Key not found in UserAgent.json: {e}\n\n"
            "Make sure the key is valid inside the file, or delete the file\n"
            f"'{global_variables.user_agent_json_file_location}'\n"
            "to create a new one by setting a new User Agent."
        )
        error_dialog.exec()


def always_on_top(window):
    if not global_variables.is_on_top:
        window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        window.q_action_always_on_top.setText("Always on Top: On")
        global_variables.is_on_top = True
    else:
        window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
        window.q_action_always_on_top.setText("Always on Top: Off")
        global_variables.is_on_top = False
    window.show()
