# LethalCompanySaveEditor GUI

**A simple save editor for Lethal Company, written in Python 3.11 for python versions higher than 3.10**
This should work for any project that utilizes ES3 Saves with encryption, you'll need the save location and the decryption password for the game you wish to edit.

This is the **GUI** version. If you're looking for the CLI version, you can find it [**here**](https://github.com/BEMZ01/LethalCompanySaveEditor/tree/master).

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
- ~~GUI~~ Added 12.01.2024
- Some way to easily define Vector3 coordinates

## Usage
1. **Create a virtual environment (Suggested)**
2. **Install the required libraries:**

   ```bash
   pip install -r "requirements.txt"
   ```
3. **Run the program:**
   ```bash
   python main.py [-p decryption_password] [-sf save_folder]
   ```

## Notes
- Backup your save files before making any changes!
- The program is currently in development and may have bugs.
- Use this program at your own risk.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Text exports

Below is a list of saves that have been exported to text via the program, feel free to use them to test the program or to see what the save file looks like.

#### Basic save with 2 apparatuses
```json
{"CurrentPlanetID":{"__type":"int","value":3},"DeadlineTime":{"__type":"int","value":3240},"EnemyScans":{"__type":"System.Int32[],mscorlib","value":[15,13,14,3,16,5,0,4]},"FileGameVers":{"__type":"int","value":45},"GroupCredits":{"__type":"int","value":116},"ProfitQuota":{"__type":"int","value":244},"QuotaFulfilled":{"__type":"int","value":0},"QuotasPassed":{"__type":"int","value":1},"RandomSeed":{"__type":"int","value":97682829},"ShipUnlockMoved_Cupboard":{"__type":"bool","value":true},"ShipUnlockMoved_Light switch":{"__type":"bool","value":true},"ShipUnlockMoved_Loud horn":{"__type":"bool","value":true},"ShipUnlockMoved_Teleporter":{"__type":"bool","value":true},"ShipUnlockMoved_Terminal":{"__type":"bool","value":true},"ShipUnlockPos_Cupboard":{"__type":"Vector3","value":{"x":7.568144,"y":1.63693845,"z":-16.7935486}},"ShipUnlockPos_Light switch":{"__type":"Vector3","value":{"x":11.01549,"y":3.74941587,"z":-13.2114782}},"ShipUnlockPos_Loud horn":{"__type":"Vector3","value":{"x":5.877596,"y":1.54161429,"z":-17.0593548}},"ShipUnlockPos_Teleporter":{"__type":"Vector3","value":{"x":5.67885256,"y":2.14171457,"z":-12.2461662}},"ShipUnlockPos_Terminal":{"__type":"Vector3","value":{"x":10.179327,"y":1.92971718,"z":-11.5579805}},"ShipUnlockRot_Cupboard":{"__type":"Vector3","value":{"x":270,"y":179.588562,"z":0}},"ShipUnlockRot_Light switch":{"__type":"Vector3","value":{"x":270,"y":260.14035,"z":0}},"ShipUnlockRot_Loud horn":{"__type":"Vector3","value":{"x":270,"y":183.371933,"z":0}},"ShipUnlockRot_Teleporter":{"__type":"Vector3","value":{"x":270,"y":64.7,"z":0}},"ShipUnlockRot_Terminal":{"__type":"Vector3","value":{"x":270,"y":350.75882,"z":0}},"ShipUnlockStored_Bunkbeds":{"__type":"bool","value":true},"ShipUnlockStored_Cupboard":{"__type":"bool","value":false},"ShipUnlockStored_File Cabinet":{"__type":"bool","value":true},"ShipUnlockStored_Goldfish":{"__type":"bool","value":false},"ShipUnlockStored_Inverse Teleporter":{"__type":"bool","value":false},"ShipUnlockStored_JackOLantern":{"__type":"bool","value":false},"ShipUnlockStored_Loud horn":{"__type":"bool","value":false},"ShipUnlockStored_Plushie pajama man":{"__type":"bool","value":false},"ShipUnlockStored_Record player":{"__type":"bool","value":false},"ShipUnlockStored_Romantic table":{"__type":"bool","value":false},"ShipUnlockStored_Shower":{"__type":"bool","value":false},"ShipUnlockStored_Signal translator":{"__type":"bool","value":false},"ShipUnlockStored_Table":{"__type":"bool","value":false},"ShipUnlockStored_Teleporter":{"__type":"bool","value":false},"ShipUnlockStored_Television":{"__type":"bool","value":false},"ShipUnlockStored_Toilet":{"__type":"bool","value":false},"ShipUnlockStored_Welcome mat":{"__type":"bool","value":false},"Stats_DaysSpent":{"__type":"int","value":4},"Stats_Deaths":{"__type":"int","value":0},"Stats_StepsTaken":{"__type":"int","value":29336},"Stats_ValueCollected":{"__type":"int","value":665},"StoryLogs":{"__type":"System.Int32[],mscorlib","value":[0,6]},"UnlockedShipObjects":{"__type":"System.Int32[],mscorlib","value":[0,1,2,3,5,7,8,11,15,16,18]},"shipGrabbableItemIDs":{"__type":"System.Int32[],mscorlib","value":[10,57,7,7,9,14,9,9,10,9,14,14]},"shipGrabbableItemPos":{"__type":"UnityEngine.Vector3[],UnityEngine.CoreModule","value":[{"x":7.978323,"y":1.357842,"z":-16.8466},{"x":6.84798431,"y":0.559296131,"z":-16.6242027},{"x":-3.66072845,"y":0.506222248,"z":-13.9978933},{"x":-3.13606262,"y":0.506222248,"z":-14.1138687},{"x":7.51461029,"y":1.85879278,"z":-16.86476},{"x":7.464815,"y":2.52133226,"z":-16.8023663},{"x":8.295965,"y":1.7387929,"z":-16.9431248},{"x":7.01499557,"y":1.85879278,"z":-16.9921741},{"x":7.1845665,"y":1.357842,"z":-16.6289959},{"x":7.870886,"y":1.85879278,"z":-16.9591885},{"x":6.893564,"y":2.42568541,"z":-17.0349121},{"x":7.824463,"y":2.52133226,"z":-16.82979}]},"shipItemSaveData":{"__type":"System.Int32[],mscorlib","value":[2]},"shipScrapValues":{"__type":"System.Int32[],mscorlib","value":[80,80]}}
```

#### A setup ready for 4 players
```json
{"CurrentPlanetID":{"__type":"int","value":3},"DeadlineTime":{"__type":"int","value":3240},"EnemyScans":{"__type":"System.Int32[],mscorlib","value":[15,13,14,3,16,5,0,4,6,1,7]},"FileGameVers":{"__type":"int","value":45},"GroupCredits":{"__type":"int","value":833},"ProfitQuota":{"__type":"int","value":591},"QuotaFulfilled":{"__type":"int","value":0},"QuotasPassed":{"__type":"int","value":3},"RandomSeed":{"__type":"int","value":2412159},"ShipUnlockMoved_Cupboard":{"__type":"bool","value":true},"ShipUnlockMoved_Goldfish":{"__type":"bool","value":true},"ShipUnlockMoved_Inverse Teleporter":{"__type":"bool","value":true},"ShipUnlockMoved_Light switch":{"__type":"bool","value":true},"ShipUnlockMoved_Loud horn":{"__type":"bool","value":true},"ShipUnlockMoved_Signal translator":{"__type":"bool","value":true},"ShipUnlockMoved_Teleporter":{"__type":"bool","value":true},"ShipUnlockMoved_Television":{"__type":"bool","value":true},"ShipUnlockMoved_Terminal":{"__type":"bool","value":true},"ShipUnlockMoved_Welcome mat":{"__type":"bool","value":true},"ShipUnlockPos_Cupboard":{"__type":"Vector3","value":{"x":7.31643343,"y":1.63763463,"z":-16.9174538}},"ShipUnlockPos_Goldfish":{"__type":"Vector3","value":{"x":10.3073874,"y":2.760485,"z":-13.3254519}},"ShipUnlockPos_Inverse Teleporter":{"__type":"Vector3","value":{"x":2.742992,"y":2.14171457,"z":-13.0040865}},"ShipUnlockPos_Light switch":{"__type":"Vector3","value":{"x":11.01549,"y":3.74941587,"z":-13.2114782}},"ShipUnlockPos_Loud horn":{"__type":"Vector3","value":{"x":5.877596,"y":1.54161429,"z":-17.0593548}},"ShipUnlockPos_Signal translator":{"__type":"Vector3","value":{"x":7.044799,"y":0.5210928,"z":-11.19898}},"ShipUnlockPos_Teleporter":{"__type":"Vector3","value":{"x":4.70941639,"y":2.14171457,"z":-12.8421249}},"ShipUnlockPos_Television":{"__type":"Vector3","value":{"x":10.6104879,"y":1.95212674,"z":-13.2053919}},"ShipUnlockPos_Terminal":{"__type":"Vector3","value":{"x":10.179327,"y":1.92971718,"z":-11.5579805}},"ShipUnlockPos_Welcome mat":{"__type":"Vector3","value":{"x":-4.99567175,"y":0.346222043,"z":-14.2044926}},"ShipUnlockRot_Cupboard":{"__type":"Vector3","value":{"x":270,"y":179.588562,"z":0}},"ShipUnlockRot_Goldfish":{"__type":"Vector3","value":{"x":270,"y":0,"z":0}},"ShipUnlockRot_Inverse Teleporter":{"__type":"Vector3","value":{"x":270,"y":64.7,"z":0}},"ShipUnlockRot_Light switch":{"__type":"Vector3","value":{"x":270,"y":260.14035,"z":0}},"ShipUnlockRot_Loud horn":{"__type":"Vector3","value":{"x":270,"y":183.371933,"z":0}},"ShipUnlockRot_Signal translator":{"__type":"Vector3","value":{"x":270,"y":92.971,"z":0}},"ShipUnlockRot_Teleporter":{"__type":"Vector3","value":{"x":270,"y":64.7,"z":0}},"ShipUnlockRot_Television":{"__type":"Vector3","value":{"x":-3.41509462e-06,"y":275.174683,"z":89.9951553}},"ShipUnlockRot_Terminal":{"__type":"Vector3","value":{"x":270,"y":350.75882,"z":0}},"ShipUnlockRot_Welcome mat":{"__type":"Vector3","value":{"x":270,"y":0,"z":0}},"ShipUnlockStored_Bunkbeds":{"__type":"bool","value":true},"ShipUnlockStored_Cupboard":{"__type":"bool","value":false},"ShipUnlockStored_File Cabinet":{"__type":"bool","value":true},"ShipUnlockStored_Goldfish":{"__type":"bool","value":false},"ShipUnlockStored_Inverse Teleporter":{"__type":"bool","value":false},"ShipUnlockStored_JackOLantern":{"__type":"bool","value":false},"ShipUnlockStored_Loud horn":{"__type":"bool","value":false},"ShipUnlockStored_Plushie pajama man":{"__type":"bool","value":false},"ShipUnlockStored_Record player":{"__type":"bool","value":false},"ShipUnlockStored_Romantic table":{"__type":"bool","value":false},"ShipUnlockStored_Shower":{"__type":"bool","value":false},"ShipUnlockStored_Signal translator":{"__type":"bool","value":false},"ShipUnlockStored_Table":{"__type":"bool","value":false},"ShipUnlockStored_Teleporter":{"__type":"bool","value":false},"ShipUnlockStored_Television":{"__type":"bool","value":false},"ShipUnlockStored_Toilet":{"__type":"bool","value":false},"ShipUnlockStored_Welcome mat":{"__type":"bool","value":false},"Stats_DaysSpent":{"__type":"int","value":13},"Stats_Deaths":{"__type":"int","value":8},"Stats_StepsTaken":{"__type":"int","value":130786},"Stats_ValueCollected":{"__type":"int","value":2665},"StoryLogs":{"__type":"System.Int32[],mscorlib","value":[0,6]},"UnlockedShipObjects":{"__type":"System.Int32[],mscorlib","value":[0,1,2,3,5,6,7,8,11,15,16,17,18,19,21,22]},"shipGrabbableItemIDs":{"__type":"System.Int32[],mscorlib","value":[10,9,15,10,9,10,12,12,9,14,14,9,14,5,5,14]},"shipGrabbableItemPos":{"__type":"UnityEngine.Vector3[],UnityEngine.CoreModule","value":[{"x":7.477545,"y":1.35853815,"z":-16.809391},{"x":6.685484,"y":1.859488,"z":-16.98854},{"x":7.663727,"y":0.719992161,"z":-16.9423981},{"x":8.042654,"y":1.25853825,"z":-16.8445415},{"x":6.95417,"y":1.7394886,"z":-17.1565762},{"x":6.6861515,"y":1.35853863,"z":-16.8820419},{"x":6.96377754,"y":3.1844945,"z":-16.8779182},{"x":8.260508,"y":3.184494,"z":-16.6893654},{"x":7.60728645,"y":1.73948908,"z":-17.151886},{"x":6.65681267,"y":2.422028,"z":-16.747673},{"x":7.72170258,"y":2.422029,"z":-16.7400265},{"x":8.044043,"y":1.7394886,"z":-17.03784},{"x":6.901497,"y":2.4224062,"z":-16.7459164},{"x":6.90683174,"y":0.5599923,"z":-16.7458782},{"x":7.26692,"y":0.629992,"z":-16.9238},{"x":7.30209541,"y":2.42246914,"z":-16.7430382}]}}
```
