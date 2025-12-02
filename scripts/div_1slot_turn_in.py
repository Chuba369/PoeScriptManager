import pyautogui
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

    vendor_lillyroth_div_turnin_x, vendor_lillyroth_div_turnin_y = config.get_xy_scaled("npc.lillyroth.div.turnin")
    vendor_lillyroth_div_reward_x, vendor_lillyroth_div_reward_y = config.get_xy_scaled("npc.lillyroth.div.reward")

    inventory_config = config.get_config_element("character.inventory.slots")
    reserved_slots  = config.get_config_element("character.inventory.reserved") or []

    usable_slots = [
        slot_id
        for slot_id in inventory_config
        if int(slot_id) not in reserved_slots
    ]

    for slot_id in usable_slots:
        if not running:
            break

        logger.info(f"Processing map at inventory slot {slot_id}")
        slot_x, slot_y = config.get_xy_scaled(f"character.inventory.slots.{slot_id}")
        logger.debug(f"inventory slot {slot_id} is assumed to be at ({slot_x}, {slot_y})")

        pyautogui.moveTo(slot_x, slot_y)
        pyperclip.copy("")
        pyautogui.hotkey('ctrl', 'c')
        div_string = pyperclip.paste()

        if not div_string.strip():
            logger.info("Inventory slot is empty. All cards processed. Stopping script.")
            winsound.MessageBeep()
            stop()
            return

        pyautogui.keyDown('ctrl')
        pyautogui.click(button="left")
        pyautogui.keyUp('ctrl')
        pyautogui.moveTo(vendor_lillyroth_div_turnin_x, vendor_lillyroth_div_turnin_y)
        pyautogui.click(button="left")
        pyautogui.moveTo(vendor_lillyroth_div_reward_x, vendor_lillyroth_div_reward_y)
        pyautogui.keyDown('ctrl')
        pyautogui.click(button="left")
        pyautogui.keyUp('ctrl')

    logger.info("Finished processing all inventory slots.")
    winsound.MessageBeep()
    stop()

def stop():
    global running
    running = False