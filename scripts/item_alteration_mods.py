import pyautogui
import pprint
from pprint import pformat
import pyperclip
import winsound

import logger
import config
import utils

running = False

def start():
    global running
    running = True

    pyautogui.PAUSE = config.get_config_element("delay.value") / 1000

    stashtab_currency_craft_x, stashtab_currency_craft_y = config.get_xy_scaled("stashtab.currency.craft")
    stashtab_currency_alteration_x, stashtab_currency_alteration_y = config.get_xy_scaled("stashtab.currency.alteration")

    desired_groups = config.get_config_element("items.mods.desired")
    mods_to_check = {
        group_name: [mod for mod in mods_list if not mod.get("ignore", False)]
        for group_name, mods_list in desired_groups.items()
    }
    logger.info("Mods to check: \n" + pprint.pformat(mods_to_check))

    pyautogui.moveTo(stashtab_currency_craft_x, stashtab_currency_craft_y)
    item_string_prev = ""

    while running:
        pyautogui.hotkey('ctrl', 'c')
        item_string = pyperclip.paste()
        logger.debug("Copied and pasted clipboard string.")
        logger.debug("Clipboard string: \n" + pprint.pformat(item_string))

        if item_string == item_string_prev:
            logger.error("Previous and current item string are identical: increase delay!")
            stop()
            return

        item_string_prev = item_string

        groups_matched = {
            group_name: utils.item_match_mods(item_string, mods)
            for group_name, mods in mods_to_check.items()
        }

        if all(groups_matched.values()):
            logger.info("Item matches all required groups; stopping script.")
            winsound.MessageBeep()
            stop()
            continue
        else:
            logger.info("Item does not match all required groups yet.")

        logger.info("Rolling item.")
        pyautogui.moveTo(stashtab_currency_alteration_x, stashtab_currency_alteration_y)
        pyautogui.click(button="right")
        pyautogui.moveTo(stashtab_currency_craft_x, stashtab_currency_craft_y)
        pyautogui.keyDown('shift')
        pyautogui.click(button="left")
        pyautogui.keyDown('alt')
        pyautogui.click(button="left")
        pyautogui.keyUp('alt')
        pyautogui.keyUp('shift')
        logger.info("Done rolling item.")

def stop():
    global running
    running = False


