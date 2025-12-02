import pyautogui
import pprint
from pprint import pformat
import pyperclip
import winsound
import requests
import math

import logger
import config
import utils

running = False

def start():
    global running
    running = True

    pyautogui.PAUSE = config.get_config_element("delay.value") / 1000

    chaos_value = config.get_config_element("poeninja.scarab.chaos_value")

    inventory_config = config.get_config_element("character.inventory.slots")
    reserved_slots  = config.get_config_element("character.inventory.reserved") or []

    usable_slots = [
        slot_id
        for slot_id in inventory_config
        if int(slot_id) not in reserved_slots
    ]

    inv_slots_available = len(usable_slots)

    scarab_data = get_scarab_prices()
    logger.debug(pprint.pformat(scarab_data))
    scarabs_over_threshhold = {name: value for name, value in scarab_data.items() if value >= chaos_value}
    logger.info(pprint.pformat(scarabs_over_threshhold))

    my_scarabs = config.get_config_element("stashtab.fragment.scarab")
    my_scarabs = {name for name in my_scarabs.items() if name in scarabs_over_threshhold}

    for name in my_scarabs.items():
        scarab_pos_x, scarab_pos_y = config.get_xy_scaled(f"stashtab.fragment.scarab.{name}")
        
        pyautogui.moveTo(scarab_pos_x, scarab_pos_y)
        pyperclip.copy("")
        pyautogui.hotkey('ctrl', 'c')
        scarab_string = pyperclip.paste()
        if scarab_string.strip():
            stacks = 0
        else: 
            parsed = utils.parse_scarab_string(scarab_string)
            stacks = math.ceil(parsed/20)

        if stacks <= inv_slots_available:
            pyautogui.keyDown('ctrl')
            pyautogui.click(button="right")
            pyautogui.keyUp('ctrl')
            inv_slots_available = inv_slots_available - stacks
            continue
        else:
            logger.info("Inventory full. Stopping script.")
            winsound.MessageBeep()
            stop()
            return

    logger.info("Finished processing all scarab slots.")
    winsound.MessageBeep()
    stop()

def stop():
    global running
    running = False

def get_scarab_prices():
    league = config.get_config_element("poeninja.league.name")
    url = f"https://poe.ninja/api/data/itemoverview?league={league}&type=Scarab"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    scarabs = {}
    for entry in data.get("lines", []):
        name = entry.get("name")
        chaos_value = entry.get("chaosValue")
        scarabs[name] = chaos_value
    return scarabs