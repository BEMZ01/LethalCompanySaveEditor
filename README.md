# LethalCompanySaveEditor

**A simple save editor for Lethal Company, written in Python 3.11 for python versions higher than 3.10**
This should work for any project that utilizes ES3 Saves with encryption, you'll need the save location and the decryption password

## How to Download

You can download the latest build of the program from the releases page [**here**](https://github.com/BEMZ01/LethalCompanySaveEditor/releases/latest).

When you first run LethalCompanySaveEditor, Windows Defender SmartScreen might display a warning message because the program is not yet widely recognized (or signed). This is a safety feature aimed at protecting you from potentially harmful applications. Click "More information" and then "Run anyway" to execute the program.
## Features

- Restore original save file
- View save file contents
- Edit save file values
- Add keys to the save file

## Future Features
- Ability to easily insert items into your save
- GUI
- Some way to easily define Vector3 coordinates

## Usage
0. **Create a virtual environment (Suggested)**
1. **Install the required libraries:**

   ```bash
   pip install -r "requirements.txt"
   ```
2. **Run the program:**
   ```bash
   python main.py [-p decryption_password] [-sf save_folder]
   ```

## Notes
- Backup your save files before making any changes!
- The program is currently in development and may have bugs.
- Use this program at your own risk.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
