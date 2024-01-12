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
import ast

server = Flask(__name__, static_folder='static', template_folder='templates')
server.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

VERSION = 1.5

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
        r = requests.get("https://raw.githubusercontent.com/BEMZ01/LethalCompanySaveEditor/gui-update/main.py")
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
    error = request.args.get('error', None)
    success = request.args.get('success', None)
    save_files = get_save_files()
    if SAVE is None:
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
    return render_template('editor.html', save=save_data, error=error, success=success)


@server.route('/save/<int:save_id>/close')
def save_close(save_id):
    global SAVE
    global ORIGINAL_SAVE
    SAVE = None
    ORIGINAL_SAVE = None
    return redirect(url_for('index', success="File closed successfully! (Not saved)"))


@server.route('/save/<int:save_id>/restore')
def save_restore(save_id):
    global SAVE
    global ORIGINAL_SAVE
    SAVE = copy.deepcopy(ORIGINAL_SAVE)
    return redirect(url_for('save', success="Save file restored successfully!", save_id=save_id))


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
        return "Invalid save file ID. Please select a valid save file."
    if SAVE is None and not bypass_none_check:
        return "Error decrypting save file. SAVE is None."
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
        return redirect(url_for('save', error="Error encrypting save file.", save_id=save_id))
    return redirect(url_for('index', success="Save file saved successfully!"))


def get_save_files():
    return [f for f in os.listdir(SAVE_FOLDER) if os.path.isfile(os.path.join(SAVE_FOLDER, f)) and f.startswith("LC")]


@server.route('/save/<int:save_id>/raw', methods=['POST', 'GET'])
def save_raw(save_id):
    global SAVE
    global ORIGINAL_SAVE
    if save_id_valid(save_id) is not None:
        return redirect(url_for('index', error=save_id_valid(save_id)))
    if request.method == 'POST':
        pprint(request.form['textarea'].strip())
        try:
            print(demjson3.decode(request.form['textarea'].strip()))
            SAVE = demjson3.decode(request.form['textarea'].strip())
            return redirect(url_for('save', success="Save file loaded successfully!", save_id=save_id))
        except demjson3.JSONDecodeError:
            print(traceback.format_exc())
            return redirect(url_for('index', error="Error loading save file."))
    else:
        save = {}
        save['id'] = save_id
        save['name'] = get_save_files()[save_id]
        save['data'] = demjson3.encode(SAVE, compactly=False, indent_amount=2)
        # load raw.html
        return render_template('raw.html', save=save)


@server.route('/save/<int:save_id>/load', methods=['POST', 'GET'])
def save_load(save_id):
    global SAVE
    global ORIGINAL_SAVE
    if save_id_valid(save_id) is not None:
        return redirect(url_for('index', error=save_id_valid(save_id)))
    if request.method == 'POST':
        try:
            SAVE = demjson3.decode(request.form['textarea'].strip())
            return redirect(url_for('save', success="Save file loaded successfully!", save_id=save_id))
        except demjson3.JSONDecodeError:
            print(traceback.format_exc())
            return redirect(url_for('index', error="Error loading save file."))
    else:
        save = {}
        save['id'] = save_id
        save['name'] = get_save_files()[save_id]
        save['data'] = demjson3.encode(SAVE, compactly=False, indent_amount=4)
        # load load.html
        return render_template('import.html', save=save)


@server.route('/save/<int:save_id>/export')
def save_export(save_id):
    global SAVE
    global ORIGINAL_SAVE
    if save_id_valid(save_id) is not None:
        return redirect(url_for('index', error=save_id_valid(save_id)))
    save = {"id": save_id, "name": get_save_files()[save_id], "data": demjson3.encode(SAVE)}
    return render_template('export.html', save=save)


@server.route('/save/<int:save_id>/insert', methods=['POST', 'GET'])
def save_insert(save_id):
    return redirect(url_for('save', error="Not implemented yet", save_id=save_id))


def value_is_valid(value, type):
    """
    Checks if a value is valid for a given type.
    :param value: The value to check
    :param type: The type to check against
    :return: None if valid, error message if invalid
    """
    try:
        if type == 'int':
            int(value)
        elif type == 'bool':
            if value.lower() not in ['true', 'false']:
                return "Boolean values must be either true or false."
        elif type == 'Vector3':
            # dict containing x, y, and z keys
            if value.count(',') != 2:
                return "Vector3 values must have 2 commas."
            v = ast.literal_eval(value)
            float(v['x'])
            float(v['y'])
            float(v['z'])
        elif type == 'System.Int32[],mscorlib':
            v = ast.literal_eval(value)
            for i in v:
                int(i)
        elif type == 'UnityEngine.Vector3[],UnityEngine.CoreModule':
            if value.count(',') < 2 and value.count('[') != value.count(']') and value.count('{') != value.count('}'):
                return ("UnityEngine.Vector3[],UnityEngine.CoreModule values must have at least 2 commas and balanced "
                        "brackets.")
            v = ast.literal_eval(value)
            for i in v:
                float(i['x'])
                float(i['y'])
                float(i['z'])
        else:
            return f"Unknown type: {type}"
    except:
        return f"Error converting value to type {type}. {traceback.format_exc()}"
    return None


def process_value(value, type):
    """
    Processes a value to the correct type.
    :param value: The value to process
    :param type: The type to process to
    :return: The processed value
    """
    if type == 'int':
        return int(value)
    elif type == 'bool':
        return value.lower() == 'true'
    elif type == 'Vector3':
        # dict containing x, y, and z keys
        v = ast.literal_eval(value)
        v['x'] = float(v['x'])
        v['y'] = float(v['y'])
        v['z'] = float(v['z'])
        return v
    elif type == 'System.Int32[],mscorlib':
        v = ast.literal_eval(value)
        for i in range(len(v)):
            v[i] = int(v[i])
        return v
    elif type == 'UnityEngine.Vector3[],UnityEngine.CoreModule':
        v = ast.literal_eval(value)
        for i in range(len(v)):
            v[i]['x'] = float(v[i]['x'])
            v[i]['y'] = float(v[i]['y'])
            v[i]['z'] = float(v[i]['z'])
        return v
    else:
        return value


@server.route('/save/<int:save_id>/modify', methods=['POST', 'GET'])
def save_modify(save_id):
    global SAVE
    global ORIGINAL_SAVE
    if save_id_valid(save_id) is not None:
        return redirect(url_for('index', error=save_id_valid(save_id)))
    if request.method == 'POST':
        new_data = {}
        r = request.form.to_dict()
        r = {k: r[k] for k in sorted(r)}
        # how many keys beginning with K are there?
        keys_length = len([k for k in r.keys() if k.startswith('K')])
        values_length = len([k for k in r.keys() if k.startswith('V')])
        if keys_length != values_length:
            return redirect(url_for('save', error="Error reading input table. Keys and values are not equal.",
                                    save_id=save_id))
        for i in range(keys_length):
            key = list(r.keys())[i]
            value = list(r.keys())[i + keys_length]
            value = r[value]
            type = list(r.keys())[i + keys_length].split('_')[1]
            key = key.split('_')[1]
            if value_is_valid(value, type) is not None:
                return redirect(url_for('save', error=value_is_valid(value, type), save_id=save_id))
            new_data[key] = {'__type': type, 'value': value}
        for k in new_data.keys():
            SAVE[k] = {"__type": new_data[k]["__type"],
                       "value": process_value(new_data[k]["value"], new_data[k]["__type"])}
        return redirect(url_for('save', success="Save file modified successfully!", save_id=save_id))

    else:
        save = {'id': save_id, 'name': get_save_files()[save_id], 'data': SAVE, 'keys': list(SAVE.keys())}
        return render_template('modify.html', save=save)


if __name__ == "__main__":
    print(f"Flags: {sys.argv}")
    print(f"Data location: {DATA_FOLDER}\n"
          f"Save files location: {SAVE_FOLDER}\n"
          f"Using password: {PASSWORD} (To change use the -p flag)\n")
    webview.create_window('LCSE', server)
    webview.start()
    raise SystemExit
