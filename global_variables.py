from pathlib import Path

url = "https://universe.flyff.com/play"
icon = "icons/PyFlyff.ico"

default_user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"

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

# Diretório Documentos do usuário
documents_folder = Path.home() / "Documents"

data_folder = documents_folder / "PyFlyff"
profile_file_location = data_folder / "profiles.txt"

mini_ftool_json_file = "MiniFToolConfig.json"
mini_ftool_json_file_location = Path(mini_ftool_json_file)

alt_control_json_file = "AltControl.json"
alt_control_json_file_location = Path(alt_control_json_file)

user_agent_json_file = "UserAgent.json"
user_agent_json_file_location = Path(user_agent_json_file)
