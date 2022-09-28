from tkinter import messagebox
import globalVariables
import json


def save_config_json(**kwargs):
    file = kwargs.get("file")
    values = kwargs.get("values")

    data = ""

    try:
        if file == globalVariables.mini_ftool_json_file:
            data = {"activation_key": values[0], "in_game_key": values[1], "repeat_times": values[2],
                    "interval": values[3], "min_interval": values[4], "fix_loop": values[5], "window": values[6]}

        if file == globalVariables.alt_control_json_file:
            data = {"activation_key": values[0], "in_game_key": values[1], "alt_window": values[2]}

        if file == globalVariables.user_agent_json_file:
            data = {"user_agent": values[0]}

        json_data = json.dumps(data)
        save_json = open(file, "w")
        save_json.write(str(json_data))
        save_json.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))
