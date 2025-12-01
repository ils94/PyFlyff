import os
import global_variables


def save_alt_profiles(combobox):
    exist = any(combobox in string for string in global_variables.profile_list)

    if not exist:
        global_variables.profile_list.append(combobox)

        f = open(global_variables.profile_file_location, "a")
        f.write(combobox + "\n")
        f.close()

        return global_variables.profile_list
    return ""


def load_alt_profiles():
    if os.path.isfile(global_variables.profile_file_location):
        f = open(global_variables.profile_file_location, "r")
        content = f.read()
        global_variables.profile_list = content.split("\n")
        if "" in global_variables.profile_list:
            global_variables.profile_list.remove("")
        f.close()
    else:
        if not os.path.isdir(global_variables.data_folder):
            os.makedirs(global_variables.data_folder)
            f = open(global_variables.profile_file_location, "w")
            f.close()
