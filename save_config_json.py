import json
from PyQt6.QtWidgets import QMessageBox
import global_variables


def save_config_json(**kwargs):
    file = kwargs.get("file")
    values = kwargs.get("values")

    data = {}

    try:
        if file == global_variables.mini_ftool_json_file:
            data = {
                "activation_key": values[0],
                "in_game_key": values[1],
                "repeat_times": values[2],
                "interval": values[3],
                "min_interval": values[4],
                "fix_loop": values[5],
                "window": values[6]
            }

        elif file == global_variables.alt_control_json_file:
            data = {
                "activation_key": values[0],
                "in_game_key": values[1],
                "alt_window": values[2]
            }

        elif file == global_variables.user_agent_json_file:
            data = {"user_agent": values[0]}

        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    except Exception as e:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Erro")
        msg.setText("Ocorreu um erro ao salvar a configuração:")
        msg.setDetailedText(str(e))
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
