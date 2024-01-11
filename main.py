#  A Lethal Company Save Editor
#  Author: BEMZlabs
import copy
import os
import sys
from pprint import pprint
import requests
import demjson3
from utils.encryption import decrypt, encrypt
from termcolor import colored
import traceback
import pyperclip
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify
import webview

server = Flask(__name__, static_folder='static', template_folder='templates')

VERSION = 1.2

os.system('color')
PASSWORD = "lcslime14a5"
DATA_FOLDER = os.path.join(os.getenv("APPDATA"), "BEMZlabs", "LCSE")
if not os.path.exists(DATA_FOLDER):
    print("Data folder not found. Creating...")
    os.makedirs(os.path.join(os.getenv("APPDATA"), "BEMZlabs", "LCSE"))
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


def check_for_updates():
    """Checks for updates to the save editor by downloading main.py from the github repo and comparing the version
    number in the second line."""
    try:
        r = requests.get("https://raw.githubusercontent.com/BEMZ01/LethalCompanySaveEditor/master/main.py")
        if r.status_code != 200:
            print("UPDATE: Error checking for updates. Status code not okay.")
            return False
        online_version = float(r.text.split('\n')[14].split(' = ')[1])
        local_version = float(VERSION)
        if online_version > local_version:
            print("UPDATE: Update available!")
            return online_version
        elif online_version == local_version:
            print("UPDATE: No updates available.")
            return False
        elif online_version < local_version:
            print("UPDATE: You are running a newer version than the latest release.")
            return False
    except requests.exceptions.ConnectionError:
        print(f"UPDATE: Error checking for updates.\n{traceback.format_exc()}")
        return False


@server.route('/')
def index():
    global SAVE, ORIGINAL_SAVE
    error = request.args.get('error', None)
    success = request.args.get('success', None)
    SAVE = None
    ORIGINAL_SAVE = None
    save_files = [f for f in os.listdir(SAVE_FOLDER) if
                  os.path.isfile(os.path.join(SAVE_FOLDER, f)) and f.startswith("LC")]
    saves = [{"id": i, "filename": f} for i, f in enumerate(save_files)]
    return render_template('index.html', saves=saves, error=error, success=success,
                           update_available=check_for_updates() is not False)


@server.route('/save/<int:save_id>')
def save(save_id):
    global SAVE
    global ORIGINAL_SAVE
    save_files = [f for f in os.listdir(SAVE_FOLDER) if
                  os.path.isfile(os.path.join(SAVE_FOLDER, f)) and f.startswith("LC")]
    SAVE = decrypt(os.path.join(SAVE_FOLDER, save_files[save_id]), PASSWORD)
    ORIGINAL_SAVE = copy.deepcopy(SAVE)
    save_data = {
        "id": save_id,
        "name": save_files[save_id],
        "stats": {
            "keys": len(SAVE.keys())}
    }
    try:
        save_data["stats"]["daysspent"] = SAVE["Stats_DaysSpent"]["value"]
        save_data["stats"]["deaths"] = SAVE["Stats_Deaths"]["value"]
        save_data["stats"]["stepstaken"] = SAVE["Stats_StepsTaken"]["value"]
        save_data["stats"]["valuecollected"] = SAVE["Stats_ValueCollected"]["value"]
    except KeyError as e:
        print(f"Error getting stats.\n{traceback.format_exc()}")
        save_data["stats"]["daysspent"] = None
        save_data["stats"]["deaths"] = None
        save_data["stats"]["stepstaken"] = None
        save_data["stats"]["valuecollected"] = None
    return render_template('editor.html', save=save_data)


@server.route('/save/<int:save_id>/close')
def save_close(save_id):
    global SAVE
    SAVE = None
    return redirect(url_for('index', success="Save file closed successfully!"))


@server.route('/save/<int:save_id>/restore')
def save_restore(save_id):
    global SAVE
    global ORIGINAL_SAVE
    SAVE = copy.deepcopy(ORIGINAL_SAVE)
    return redirect(url_for('index', success="Save file restored successfully!"))


def save_id_valid(save_id, bypass_none_check=False):
    """
    Checks if a save ID is valid.
    :param bypass_none_check: Whether to bypass the check for if the save file is decrypted
    :param save_id: The save ID to check
    :return: None if valid, error message if invalid
    """
    global SAVE
    save_files = get_save_files()
    if save_id >= len(save_files) or save_id < 0:
        return "Invalid save file ID."
    if SAVE is None and not bypass_none_check:
        return "Error decrypting save file."
    if "LastVerPlayed" not in SAVE.keys() and "FileGameVers" not in SAVE.keys():
        return ("Error loading save file. FileGameVers and LastVerPlayed key not found. This may not be a Lethal "
                "Company save.")
    return None


@server.route('/save/<int:save_id>/save')
def save_save(save_id):
    global SAVE
    global ORIGINAL_SAVE
    if save_id_valid(save_id) is not None:
        return redirect(url_for('index', error=save_id_valid(save_id)))
    save_files = get_save_files()
    save_file_path = os.path.join(SAVE_FOLDER, save_files[save_id])
    if not encrypt(save_file_path, SAVE, PASSWORD):
        return redirect(url_for('index', error="Error encrypting save file."))
    return redirect(url_for('index', success="Save file saved successfully!"))


def get_save_files():
    return [f for f in os.listdir(SAVE_FOLDER) if os.path.isfile(os.path.join(SAVE_FOLDER, f)) and f.startswith("LC")]


@server.route('/save/<int:save_id>/raw')
def save_raw(save_id):
    global SAVE
    if save_id_valid(save_id) is not None:
        return redirect(url_for('index', error=save_id_valid(save_id)))
    return jsonify(SAVE)


@server.route('/save/<int:save_id>/load', methods=['POST', 'GET']
def save_load(save_id):
    global SAVE
    global ORIGINAL_SAVE
    if save_id_valid(save_id) is not None:
        return redirect(url_for('index', error=save_id_valid(save_id)))
    if request.method == 'POST':
        ...
        return redirect(url_for('save', save_id=save_id, success="Save file loaded successfully!"))
    else:
        return render_template('load.html')


@server.route('/save/<int:save_id>/insert')
def save_insert(save_id):
    print("Not implemented yet")
    return redirect(url_for('index', error="Not implemented yet"))


@server.route('/save/<int:save_id>/modify')
def save_modify(save_id):
    print("Not implemented yet")
    return redirect(url_for('index', error="Not implemented yet"))


if __name__ == "__main__":
    print(f"Flags: {sys.argv}")
    print(f"Data location: {DATA_FOLDER}\n"
          f"Save files location: {SAVE_FOLDER}\n"
          f"Using password: {PASSWORD} (To change use the -p flag)\n")
    webview.create_window('LCSE', server)
    webview.start()


    ORIGINAL_SAVE = copy.deepcopy(SAVE)
    SNAPSHOTS = []
    if SAVE is None:
        input("Error decrypting save file. SAVE is None. Press enter to continue...")
        exit(1)
    if "LastVerPlayed" not in SAVE.keys() and "FileGameVers" not in SAVE.keys():
        print("Error loading save file. FileGameVers and LastVerPlayed key not found. This may not be a Lethal"
              " Company save.")
    print(f"Save file {save_file} decrypted and loaded successfully! ({len(SAVE.keys())} keys)")
    while True:
        input("Press enter to continue...")
        clear_screen()
        menu = input("Actions:\n"
                     "0: Restore original save file\n"
                     "1: View save file\n"
                     "2: Edit save file\n"
                     "3: Add key to save file\n"
                     "4: Take snapshot of save file\n"
                     "5: Revert to a snapshot\n"
                     "6: Save to external file (for sharing)\n"
                     "7: Export save file to text (for sharing)\n"
                     "8: Import save file from URL\n"
                     "9: Import save file from text\n"
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
        elif menu == "4":
            # take snapshot of save file
            SNAPSHOTS.append(copy.deepcopy(SAVE))
            print(f"Snapshot taken. ID {len(SNAPSHOTS) - 1}")
        elif menu == "5":
            # revert to snapshot
            while True:
                try:
                    snapshot = int(input("Enter the snapshot ID to revert to: "))
                except ValueError or TypeError as e:
                    print("Invalid snapshot ID.")
                    continue
                if snapshot < 0 or snapshot >= len(SNAPSHOTS):
                    print("Invalid snapshot ID.")
                    continue
                break
            SAVE = copy.deepcopy(SNAPSHOTS[snapshot])
            print("Save file reverted.")
        elif menu == "6":
            # save to external file
            while True:
                file_name = input("Enter the file name to save to: ")
                if file_name == "":
                    print("Invalid file name.")
                    continue
                break
            with open(os.path.join(DATA_FOLDER, file_name), "w") as f:
                f.write(str(SAVE))
            print("Save file saved.")
        elif menu == "7":
            # export save file to text
            # convert save to json
            pyperclip.copy(demjson3.encode(SAVE))
            print(f"Save copied to clipboard. \n{demjson3.encode(SAVE)}")

        elif menu == "8":
            # override save file with online save file
            SNAPSHOTS.append(copy.deepcopy(SAVE))
            while True:
                url = input("Enter the URL of the save file to load: ")
                if url == "":
                    print("Invalid URL.")
                    continue
                break
            r = requests.get(url)
            if r.status_code != 200:
                print("Error downloading save file.")
                continue
            try:
                SAVE = demjson3.decode(r.text)
            except demjson3.JSONDecodeError as e:
                print("Error decoding save file.")
                continue
            if "LastVerPlayed" not in SAVE.keys() and "FileGameVers" not in SAVE.keys():
                print("Error loading save file. FileGameVers and LastVerPlayed key not found. This may not be"
                      " a Lethal Company save.")
            print(f"Save loaded successfully! ({len(SAVE.keys())} keys)")
        elif menu == "9":
            # override save file with text
            SNAPSHOTS.append(copy.deepcopy(SAVE))
            while True:
                text = input("Enter the save file text to load: ")
                if text == "":
                    print("Invalid text.")
                    continue
                break
            try:
                SAVE = demjson3.decode(text)
            except demjson3.JSONDecodeError as e:
                print("Error decoding save file.")
                continue
            if "LastVerPlayed" not in SAVE.keys() and "FileGameVers" not in SAVE.keys():
                print("Error loading save file. FileGameVers and LastVerPlayed key not found. This may not be a Lethal"
                      " Company save.")
            print(f"Save loaded successfully! ({len(SAVE.keys())} keys)")
        elif menu == "s":
            break
        elif menu == "q":
            print("Exiting without saving...")
            exit(0)
        else:
            print("Invalid action.")
