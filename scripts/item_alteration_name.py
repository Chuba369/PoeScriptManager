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
 
    desired_group1 = config.get_config_element("items.name.desired.group1")
    logger.info("Mods to check for group1: " + pprint.pformat(desired_group1))
    desired_group2 = config.get_config_element("items.name.desired.group2")
    logger.info("Mods to check for group2: " + pprint.pformat(desired_group2))

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

        if utils.item_match_name(item_string, desired_group1, desired_group2):
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


