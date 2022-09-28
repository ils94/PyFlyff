import os
import globalVariables


def save_alt_profiles(combobox):
    exist = any(combobox in string for string in globalVariables.profile_list)

    if not exist:
        globalVariables.profile_list.append(combobox)

        f = open(globalVariables.profile_file_location, "a")
        f.write(combobox + "\n")
        f.close()

        return globalVariables.profile_list


def load_alt_profiles():
    if os.path.isfile(globalVariables.profile_file_location):
        f = open(globalVariables.profile_file_location, "r")
        content = f.read()
        globalVariables.profile_list = content.split("\n")
        if "" in globalVariables.profile_list:
            globalVariables.profile_list.remove("")
        f.close()
    else:
        if not os.path.isdir(globalVariables.data_folder):
            os.makedirs(globalVariables.data_folder)
            f = open(globalVariables.profile_file_location, "w")
            f.close()
