import pyautogui
import pprint
from pprint import pformat
import pyperclip
import winsound

import logger
import config

running = False

def start():
    global running
    running = True

    pyautogui.PAUSE = config.get_config_element("delay.value") / 1000

    stashtab_currency_craft_x, stashtab_currency_craft_y = config.get_xy_scaled("stashtab.currency.craft")
    stashtab_currency_chance_x, stashtab_currency_chance_y = config.get_xy_scaled("stashtab.currency.chance")

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

        if "rarity: unique" in item_string.lower():
            logger.info("Item is unique; stopping script.")
            winsound.MessageBeep()
            stop()
            continue
        else:
            logger.info("Item is not yet unique.")

        logger.info("Rolling item.")
        pyautogui.moveTo(stashtab_currency_chance_x, stashtab_currency_chance_y)
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


