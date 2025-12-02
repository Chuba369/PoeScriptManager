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

    config_maps_mods_avoid = config.get_config_element("maps.mods.avoid")
    config_rarity = config.get_config_element("maps.mods.rarity")
    config_quantity = config.get_config_element("maps.mods.quantity")
    config_packsize = config.get_config_element("maps.mods.packsize")
    config_currency = config.get_config_element("maps.mods.currency")
    config_scarabs = config.get_config_element("maps.mods.scarabs")
    config_maps = config.get_config_element("maps.mods.maps")
    config_sum_currency_scarab = config.get_config_element("maps.mods.sum_currency_scarab")
    config_sum_currency_scarab_map = config.get_config_element("maps.mods.sum_currency_scarab_map")
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
            map_more_scarabs =parsed.get("more_scarabs", 0)
            map_more_maps = parsed.get("more_maps", 0)
            map_mods = parsed.get("modifiers", [])

            has_bad_mods, matched_mods = utils.has_bad_map_mods(map_mods, config_maps_mods_avoid)
            if not has_bad_mods:
                logger.info("Map mods are fine; Checking rarity, quantitiy, etc.")
                if (map_rarity is not None and config_rarity is not None and map_rarity >= config_rarity):
                    logger.info("Rarity is good; keeping map. Next inventory slot.")
                    finish()
                    break

                if (map_quantitiy is not None and config_quantity is not None and map_quantitiy >= config_quantity):
                    logger.info("Quantitiy is good; keeping map. Next inventory slot.")
                    finish()
                    break

                if (map_packsize is not None and config_packsize is not None and map_packsize >= config_packsize):
                    logger.info("Packsize is good; keeping map. Next inventory slot.")
                    finish()
                    break

                if (map_more_currency is not None and config_currency is not None and map_more_currency >= config_currency):
                    logger.info("Currency is good; keeping map. Next inventory slot.")
                    finish()
                    break

                if (map_more_scarabs is not None and config_scarabs is not None and map_more_scarabs >= config_scarabs):
                    logger.info("Scarabs are good; keeping map. Next inventory slot.")
                    finish()
                    break

                if (map_more_maps is not None and config_maps is not None and map_more_maps >= config_maps):
                    logger.info("Maps is good; keeping map. Next inventory slot.")
                    finish()
                    break

                if (map_more_currency is not None and map_more_scarabs is not None and config_sum_currency_scarab is not None and map_more_currency + map_more_scarabs >= config_sum_currency_scarab):
                    logger.info("Currency + scarabs is good; keeping map. Next inventory slot.")
                    finish()
                    break

                if (map_more_currency is not None and map_more_scarabs is not None and map_more_maps is not None and config_sum_currency_scarab_map is not None and map_more_currency + map_more_scarabs + map_more_maps >= config_sum_currency_scarab_map):
                    logger.info("Currency + scarabs + maps is good; keeping map. Next inventory slot.")
                    finish()
                    break

                logger.info("Map is not good enough to keep.")
            else:
                logger.info("Has bad map mods: " + str(has_bad_mods))
                logger.info("Matching mods: " + str(matched_mods))

            logger.info("Rolling map.")
            pyautogui.moveTo(stashtab_currency_chaos_x, stashtab_currency_chaos_y)
            pyautogui.click(button="right")
            pyautogui.moveTo(stashtab_currency_craft_x, stashtab_currency_craft_y)
            pyautogui.click(button="left")     
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