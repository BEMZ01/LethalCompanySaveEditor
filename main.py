#  A Lethal Company Save Editor
#  Author: BEMZlabs
import copy
import os
import sys
from pprint import pprint

import demjson3

from utils.encryption import decrypt, encrypt
from termcolor import colored

os.system('color')
PASSWORD = "lcslime14a5"
SAVE_FOLDER = os.path.join(os.getenv("USERPROFILE"), "AppData", "LocalLow", "ZeekerssRBLX", "Lethal Company")
SAVE = None
ORIGINAL_SAVE = None

RESET = {'CurrentPlanetID': {'__type': 'int', 'value': 0},
 'DeadlineTime': {'__type': 'int', 'value': 3240},
 'FileGameVers': {'__type': 'int', 'value': 45},
 'GroupCredits': {'__type': 'int', 'value': 60},
 'ProfitQuota': {'__type': 'int', 'value': 130},
 'QuotaFulfilled': {'__type': 'int', 'value': 0},
 'QuotasPassed': {'__type': 'int', 'value': 0},
 'RandomSeed': {'__type': 'int', 'value': 0},
 'ShipUnlockMoved_Cupboard': {'__type': 'bool', 'value': True},
 'ShipUnlockMoved_Terminal': {'__type': 'bool', 'value': True},
 'ShipUnlockPos_Cupboard': {'__type': 'Vector3',
                            'value': {'x': 8.619258,
                                      'y': 1.63403118,
                                      'z': -16.2241688}},
 'ShipUnlockPos_Terminal': {'__type': 'Vector3',
                            'value': {'x': 10.179327,
                                      'y': 1.92971718,
                                      'z': -11.5579805}},
 'ShipUnlockRot_Cupboard': {'__type': 'Vector3',
                            'value': {'x': 270, 'y': 179.588562, 'z': 0}},
 'ShipUnlockRot_Terminal': {'__type': 'Vector3',
                            'value': {'x': 270, 'y': 350.75882, 'z': 0}},
 'ShipUnlockStored_Bunkbeds': {'__type': 'bool', 'value': True},
 'ShipUnlockStored_Cupboard': {'__type': 'bool', 'value': False},
 'ShipUnlockStored_File Cabinet': {'__type': 'bool', 'value': True},
 'ShipUnlockStored_Goldfish': {'__type': 'bool', 'value': False},
 'ShipUnlockStored_Inverse Teleporter': {'__type': 'bool', 'value': False},
 'ShipUnlockStored_JackOLantern': {'__type': 'bool', 'value': False},
 'ShipUnlockStored_Loud horn': {'__type': 'bool', 'value': False},
 'ShipUnlockStored_Plushie pajama man': {'__type': 'bool', 'value': False},
 'ShipUnlockStored_Record player': {'__type': 'bool', 'value': False},
 'ShipUnlockStored_Romantic table': {'__type': 'bool', 'value': False},
 'ShipUnlockStored_Shower': {'__type': 'bool', 'value': False},
 'ShipUnlockStored_Signal translator': {'__type': 'bool', 'value': False},
 'ShipUnlockStored_Table': {'__type': 'bool', 'value': False},
 'ShipUnlockStored_Teleporter': {'__type': 'bool', 'value': False},
 'ShipUnlockStored_Television': {'__type': 'bool', 'value': False},
 'ShipUnlockStored_Toilet': {'__type': 'bool', 'value': False},
 'ShipUnlockStored_Welcome mat': {'__type': 'bool', 'value': False},
 'Stats_DaysSpent': {'__type': 'int', 'value': 0},
 'Stats_Deaths': {'__type': 'int', 'value': 0},
 'Stats_StepsTaken': {'__type': 'int', 'value': 362},
 'Stats_ValueCollected': {'__type': 'int', 'value': 0},
 'StoryLogs': {'__type': 'System.Int32[],mscorlib', 'value': [0]},
 'UnlockedShipObjects': {'__type': 'System.Int32[],mscorlib',
                         'value': [0, 7, 8, 15, 16]}}


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def process_value(value: dict):
    # create a value depending on the __type key
    if "__type" not in value.keys():
        print("Invalid value: missing __type key.")
        return None
    if value["__type"] == 'int':
        return int(value['value'])
    elif value["__type"] == 'bool':
        return bool(value['value'])
    elif value["__type"] == 'string':
        return str(value['value'])
    elif value["__type"] == 'float':
        return float(value['value'])
    elif value["__type"] == 'Vector3':
        return str(value['value'])
    elif value["__type"] == 'System.Int32[],mscorlib':
        return str(value['value'])
    elif value["__type"] == 'UnityEngine.Vector3[],UnityEngine.CoreModule':
        return str(value['value'])
    else:
        print(f"Invalid value: unknown __type {value['__type']}.")
        return None


def display_save(display_index: bool = False) -> bool:
    """Displays the save file in a pretty format. Green values have been modified.
    :param display_index: Whether to display the index of each key before the key name. Default: False
    :return: True if successful, False otherwise"""
    if not display_index:
        for k, v in SAVE.items():
            # if key type is not recognized
            if process_value(v) is not None:
                print(colored(k, "green" if k not in ORIGINAL_SAVE.keys() else "blue"), end="")
                print(colored(": ", "white"), end="")
                print(colored(process_value(v), "green" if k not in ORIGINAL_SAVE.keys() or v["value"] != ORIGINAL_SAVE[k]["value"] else "blue"))
    else:
        for i, (k, v) in enumerate(SAVE.items()):
            # if key type is not recognized
            if process_value(v) is not None:
                if v["value"] != ORIGINAL_SAVE[k]["value"]:
                    print(colored(f"{i}: ", "white"), end="")
                    print(colored(k, "blue"), end="")
                    print(colored(": ", "white"), end="")
                    print(colored(process_value(v), "green"), end="")
                    print(colored(f" ({process_value(ORIGINAL_SAVE[k])})", "white"))
                else:
                    print(colored(f"{i}: ", "white"), end="")
                    print(colored(k, "blue"), end="")
                    print(colored(": ", "white"), end="")
                    print(colored(process_value(v), "white"))

    return True


def edit_save():
    edits = 0
    edit = True
    while True:
        while True:
            display_save()
            key = input("Enter the key to edit: ")
            if key == "":
                edit = False
                break
            elif key not in SAVE.keys():
                print("Invalid key.")
                continue
            break
        while edit:
            value = input(f"Original type is {SAVE[key]['__type']}\nEnter the new value: ")
            expected_type = SAVE[key]["__type"]
            if value.lower() == "true" and expected_type == "bool":
                value = True
            elif value.lower() == "false" and expected_type == "bool":
                value = False
            elif value.isnumeric() and expected_type == "int":
                value = int(value)
            elif value.replace(".", "", 1).isnumeric() and expected_type == "float":
                value = float(value)
            elif expected_type == "Vector3":
                try:
                    value = dict(demjson3.decode(value))
                except demjson3.JSONDecodeError as e:
                    print("Invalid value. (Didn't match Vector3 format)")
                    continue
            elif expected_type == "System.Int32[],mscorlib":
                # System.Int32[],mscorlib is stored as [1,2,3,4,5] string
                try:
                    value = demjson3.decode(value)
                except demjson3.JSONDecodeError as e:
                    print("Invalid value. (Didn't match System.Int32[],mscorlib format)")
                    continue
            elif expected_type == "UnityEngine.Vector3[],UnityEngine.CoreModule":
                try:
                    value = demjson3.decode(value)
                except demjson3.JSONDecodeError as e:
                    print("Invalid value. (Didn't match UnityEngine.Vector3[],UnityEngine.CoreModule format)")
                    continue
            else:
                value = str(value)
            break
        if edit:
            clear_screen()
            edits += 1
            SAVE[key]["value"] = value
            print("Value updated.")
        # ask if user wants to continue editing
        while True:
            cont = input(f"You've made {edits} edits.\nContinue editing? (Y/N): ").upper()
            if cont == "Y":
                break
            elif cont == "N":
                return True
            else:
                print("Invalid option.")
        clear_screen()


def add_keys():
    # add keys to the save file
    global SAVE
    while True:
        while True:
            display_save()
            key = input("Enter the key to add: ")
            if key == "":
                return True
            elif key in SAVE.keys():
                print("Key already exists.")
                continue
            break
        while True:
            type = input("Enter the type of the key: ")
            if type == "":
                return True
            elif type == "int":
                while True:
                    try:
                        value = int(input("Enter the value of the key: "))
                        break
                    except ValueError or TypeError as e:
                        print("Invalid value.")
                        continue

            elif type == "bool":
                while True:
                    try:
                        value = True if input("Enter the value of the key: ").lower() == "true" else False
                        break
                    except ValueError or TypeError as e:
                        print("Invalid value.")
                        continue

            elif type == "string":
                while True:
                    try:
                        value = str(input("Enter the value of the key: "))
                        break
                    except ValueError or TypeError as e:
                        print("Invalid value.")
                        continue

            elif type == "float":
                while True:
                    try:
                        value = float(input("Enter the value of the key: "))
                        break
                    except ValueError or TypeError as e:
                        print("Invalid value.")
                        continue

            elif type == "Vector3":
                value = str(input("Enter the value of the key: "))
                while True:
                    try:
                        value = dict(demjson3.decode(value))
                        break
                    except demjson3.JSONDecodeError as e:
                        print("Invalid value. (Didn't match Vector3 format)")
                        continue

                break
            elif type == "System.Int32[],mscorlib":
                value = str(input("Enter the value of the key: "))
                while True:
                    try:
                        value = demjson3.decode(value)
                        break
                    except demjson3.JSONDecodeError as e:
                        print("Invalid value. (Didn't match System.Int32[],mscorlib format)")
                        continue
                break
            elif type == "UnityEngine.Vector3[],UnityEngine.CoreModule":
                value = str(input("Enter the value of the key: "))
                while True:
                    try:
                        value = demjson3.decode(value)
                        break
                    except demjson3.JSONDecodeError as e:
                        print("Invalid value. (Didn't match UnityEngine.Vector3[],UnityEngine.CoreModule format)")
                        continue
                break
            else:
                print("Invalid type.")
                continue
            break
        SAVE[key] = {"__type": type, "value": value}
        print(f"{key} = {SAVE[key]}")
        print("Key added.")
        # ask if user wants to continue adding keys
        while True:
            cont = input("Continue adding keys? (Y/N): ").upper()
            if cont == "Y":
                break
            elif cont == "N":
                return True
            else:
                print("Invalid option.")


if __name__ == "__main__":
    # Check flags for password
    if "-p" in sys.argv:
        try:
            PASSWORD = str(sys.argv[sys.argv.index("-p") + 1])
        except IndexError or ValueError as e:
            print("Invalid password.")
            exit(1)
    elif "-sf" in sys.argv:
        # save folder path flag
        try:
            SAVE_FOLDER = str(sys.argv[sys.argv.index("-sf") + 1])
        except IndexError or ValueError as e:
            print("Invalid save folder path.")
            exit(1)
    # check if save folder exists
    if not os.path.exists(SAVE_FOLDER):
        print("Save folder does not exist.")
        exit(1)
    # save files are located at %userprofile%\AppData\LocalLow\ZeekerssRBLX\Lethal Company
    # list all files starting with "LC" in the directory
    try:
        save_files = [f for f in os.listdir(SAVE_FOLDER) if
                      os.path.isfile(os.path.join(SAVE_FOLDER, f)) and f.startswith("LC")]
    except FileNotFoundError as e:
        print("Save files not found. Please run the game and generate at least 1 save file.")
        exit(1)
    print(f"Save files location: {SAVE_FOLDER}\n"
          f"Using password: {PASSWORD} (To change use the -p flag)\n")
    print("Save files found:")
    for i, f in enumerate(save_files):
        print(f"{i}: {f}")
    # ask for save file to edit
    while True:
        try:
            save_file = int(input("Enter the number of the save file to edit: "))
        except ValueError or TypeError as e:
            print("Invalid save file number.")
            continue
        if save_file < 0 or save_file >= len(save_files):
            print("Invalid save file number.")
            continue
        break
    save_file = save_files[save_file]
    save_file_path = os.path.join(SAVE_FOLDER, save_file)
    # ask for action
    SAVE = decrypt(save_file_path, PASSWORD)
    ORIGINAL_SAVE = copy.deepcopy(SAVE)
    if SAVE is None:
        print("Error decrypting save file. Exiting...")
        exit(1)
    print(f"Save file {save_file} decrypted and loaded successfully! ({len(SAVE.keys())} keys)")
    while True:
        input("Press enter to continue...")
        clear_screen()
        menu = input("Actions:\n"
                     "0: Restore original save file\n"
                     "1: View save file\n"
                     "2: Edit save file\n"
                     "3: Add key to save file\n"
                     "S: Save and exit\n"
                     "Q: Exit without saving\n"
                     "Enter the number of the action to perform: ").lower()
        clear_screen()
        if menu == "raw":
            # secret - prints raw save file
            pprint(SAVE)
        elif menu == "benboom":
            # secret - load the quick start save file
            SAVE = copy.deepcopy(RESET)
            print("Save file loaded.")
        elif menu == "0":
            SAVE = copy.deepcopy(ORIGINAL_SAVE)
            print("Save file restored.")
        elif menu == "1":
            display_save()
        elif menu == "2":
            edit_save()
        elif menu == "3":
            add_keys()
        elif menu == "s":
            break
        elif menu == "q":
            print("Exiting without saving...")
            exit(0)
        else:
            print("Invalid action.")
    # save and exit
    print("Saving and exiting...")
    encrypt(save_file_path, SAVE, PASSWORD)
    exit(0)
