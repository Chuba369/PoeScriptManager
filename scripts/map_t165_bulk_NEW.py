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
    stashtab_currency_chaos_x, stashtab_currency_chaos_y = config.get_xy_scaled("stashtab.currency.chaos")
    stashtab_currency_alchemy_x, stashtab_currency_alchemy_y = config.get_xy_scaled("stashtab.currency.alchemy")
    stashtab_currency_scour_x, stashtab_currency_scour_y = config.get_xy_scaled("stashtab.currency.scour")
    stashtab_currency_exalt_x, stashtab_currency_exalt_y = config.get_xy_scaled("stashtab.currency.exalt")

    config_maps_mods_avoid = config.get_config_element("maps.mods.avoid")
    config_currency = config.get_config_element("maps.mods.currency")
    config_scarab = config.get_config_element("maps.mods.scarabs")
    logger.info("Map mods to avoid " + str(config_maps_mods_avoid))

    inventory_config = config.get_config_element("character.inventory.slots")
    reserved_slots  = config.get_config_element("character.inventory.reserved") or []

    usable_slots = [
        slot_id
        for slot_id in inventory_config
        if int(slot_id) not in reserved_slots
    ]

    map_string_prev = ""

    for slot_id in usable_slots:
        if not running:
            break
    
        logger.info(f"Processing map at inventory slot {slot_id}")
        slot_x, slot_y = config.get_xy_scaled(f"character.inventory.slots.{slot_id}")
        logger.debug(f"inventory slot {slot_id} is assumed to be at ({slot_x}, {slot_y})")

        pyautogui.moveTo(slot_x, slot_y)
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('shift')
        pyautogui.click(button="left")
        pyautogui.keyUp('shift')
        pyautogui.keyUp('ctrl')

        while running:
            pyautogui.moveTo(stashtab_currency_craft_x, stashtab_currency_craft_y)
            pyperclip.copy("")
            pyautogui.hotkey('ctrl', 'c')
            map_string = pyperclip.paste()
            logger.debug("Copied and pasted clipboard string.")
            logger.debug("Clipboard string: \n" + pformat(map_string))
            
            if not map_string.strip():
                logger.info("Inventory slot is empty. All maps processed. Stopping script.")
                winsound.MessageBeep()
                stop()
                return

            if map_string == map_string_prev:
                logger.error("Previous and current map string are identical: increase delay!")
                stop()
                return
            
            map_string_prev = map_string
            
            parsed = utils.parse_map_string(map_string)
            logger.debug("Parsed map:\n" + pprint.pformat(parsed))

            map_rarity = parsed.get("rarity", 0)
            map_quantitiy = parsed.get("quantity", 0)
            map_packsize = parsed.get("pack_size", 0)
            map_more_currency = parsed.get("more_currency", 0)
            map_more_scarab = parsed.get("more_scarab", 0)
            map_mods = parsed.get("modifiers", [])

            has_bad_mods, matched_mods = utils.has_bad_map_mods(map_mods, config_maps_mods_avoid)
            if not has_bad_mods:
                logger.info("Map mods are fine; Checking Currency.")
                if (map_more_scarab is not None and config_scarab is not None and map_more_scarab >= config_scarab):
                    logger.info("Scarab is good; Checking sum.")
                    if (map_quantitiy + 3 * map_packsize >= 165):
                        logger.info("Sum 1 good enough; Slamming.")
                        pyautogui.moveTo(stashtab_currency_exalt_x, stashtab_currency_exalt_y)
                        pyautogui.click(button="right")
                        pyautogui.moveTo(stashtab_currency_craft_x, stashtab_currency_craft_y)
                        pyautogui.click(button="left")
                        pyautogui.moveTo(stashtab_currency_exalt_x, stashtab_currency_exalt_y)
                        pyautogui.click(button="right")
                        pyautogui.moveTo(stashtab_currency_craft_x, stashtab_currency_craft_y)
                        pyautogui.click(button="left")
                        if (map_quantitiy + 3 * map_packsize >= 195):
                            logger.info("Sum 2 good enough.")
                            finish()
                            break

                logger.info("Map is not good enough to keep.")
            else:
                logger.info("Has bad map mods: " + str(has_bad_mods))
                logger.info("Matching mods: " + str(matched_mods))

            logger.info("Rolling map.")

            pyautogui.moveTo(stashtab_currency_scour_x, stashtab_currency_scour_y)
            pyautogui.click(button="right")
            pyautogui.moveTo(stashtab_currency_craft_x, stashtab_currency_craft_y)
            pyautogui.click(button="left")
            pyautogui.moveTo(stashtab_currency_alchemy_x, stashtab_currency_alchemy_y)
            pyautogui.click(button="right")
            pyautogui.moveTo(stashtab_currency_craft_x, stashtab_currency_craft_y)
            pyautogui.click(button="left")

            #pyautogui.moveTo(stashtab_currency_chaos_x, stashtab_currency_chaos_y)
            #pyautogui.click(button="right")
            #pyautogui.moveTo(stashtab_currency_craft_x, stashtab_currency_craft_y)
            #pyautogui.click(button="left")    

            logger.info("Done rolling map.")

    logger.info("Finished processing all inventory slots.")
    winsound.MessageBeep()
    stop()

def stop():
    global running
    running = False

def finish():
    pyautogui.keyDown('ctrl')
    pyautogui.click(button="left")
    pyautogui.keyUp('ctrl')