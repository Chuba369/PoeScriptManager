# PoE Script Manager

This is a python programm that runs a gui to start and stop different scripts for Path of Exile.

## Features
- The program is flexible in its configuration by having a human readable config.json file
- The scripts are delivered with the .exe and config.json so that they can be adjusted on the fly  
- The gui can select, deselect, start and stop scripts. It can also reload the config.json without the need to restart the application. Furthermore the most relevant config elements can be changed directly via the gui.

## Available scripts
- **div_1slot_turn_in**: This will turn in your enitre inventory (except for the configured reserved slots) of div cards with rewards of stack size <= 1 e.g., Rain of Chaos
- **item_alchemy_mods**: This script will scour alch spam the item in your currency stash crafting window looking for the mods specified in the config.json (regex pattern matcher e.g., (\d+)% increased Physical Damage).
- **item_alteration_mods**: This script will alt aug spam the item in your currency stash crafting window looking for the mods specified in the config.json (regex pattern matcher e.g., (\d+)% increased Physical Damage).
- **item_alteration_name**: This script will alt aug spam the item in your currency stash crafting window looking for the names of the mods specified in the config.json (name matcher e.g., "Merciless")
- **item_chance**: This script will scour chance the item in your currency stash crafting window until it becomes unique
- **map_t17_single**: This script will chaos spam the map in your currency stash crafting window until at least 1 of the configured modifiers is fullfilled and there are no mods to avoid
- **map_t17_bulk**: This script will loop over your inventory (except for the configured reserved slots) and roll your t17 maps. Rules are identical to map_t17_single
- **map_t165_single**: This script will scour alch spam the map in your currency stash crafting window until at least 1 of the configured modifiers is fullfilled and there are no mods to avoid
- **map_t165_bulk**: This script will loop over your inventory (except for the configured reserved slots) and roll your t165 maps. Rules are identical to map_t165_single
- **scarab_get_valuable**: This script will go over the fragment-scarab tab and grab all valuable scarabs until your inventory is full or everything is processed. Exact value threshhold can be configured.

## Installation
### User
- Download the PoeScriptManager.exe, config.json and the scripts folder from the release page. 
- Put everything in the same folder e.g., PoeScritpManager.
- Run the executable.

### Developer
**Requirement**: A 64-bit installation of Python version 3.14.0 or higher.
1. clone the repo
- *git clone <repo-url>*
- *cd PoeScriptManager*
2. create and start venv (virtual python enviroment)
- *python -m venv venv*
- *venv\Scripts\activate* 
3. install development dependencies
- *pip install -r dev-requirements.txt*
4. build the .exe
- *pyinstaller --onefile main.py --name PoeScriptManager*
