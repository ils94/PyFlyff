import pathlib

url = "https://universe.flyff.com/play"
icon = "icons/PyFlyff.ico"

default_user_agent = "None"

mini_ftool_activation_key = ""
mini_ftool_min_interval = 0
fix_mini_ftool_loop_var = ""

alt_control_key_list_1 = []
alt_control_key_list_2 = []
profile_list = []
mini_ftool_global_vars = []

mini_ftool_window_name = ""
hwndMain = ""
hwndAlt = ""
alt_window_name = ""
user_agent = ""

mini_ftool_repeat_times = 0

start_mini_ftool_loop = False
alt_control_boolean = False
menubar_window = False
can_reload_client = False
is_on_top = False

data_folder = "C:/PyFlyff"
profile_file_location = "C:/PyFlyff/profiles.txt"

mini_ftool_json_file = "MiniFToolConfig.json"
mini_ftool_json_file_location = pathlib.Path(mini_ftool_json_file)

alt_control_json_file = "AltControl.json"
alt_control_json_file_location = pathlib.Path(alt_control_json_file)

user_agent_json_file = "UserAgent.json"
user_agent_json_file_location = pathlib.Path(user_agent_json_file)