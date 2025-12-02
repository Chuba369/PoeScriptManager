import json
import pprint

import logger

CONFIG_FILE = "config.json"

cfg = {}

def load_config(file_path=CONFIG_FILE):
    global cfg
    try:
        with open(file_path, "r") as f:
            cfg = json.load(f)
        logger.info(f"Configuration loaded from file.")

        if "log" in cfg and "level" in cfg["log"]:
            level = cfg["log"]["level"]
            logger.set_log_level(level)
            logger.info(f"Log level loaded from config and set to {level}")
        else:
            logger.set_log_level("INFO")
            logger.info("Log level not found in config, defaulting to INFO")

    except Exception as e:
        logger.error(f"Failed to load config from path '{file_path}': {e}")
        raise e

# Get nested config element by dot-separated path 
def get_config_element(path):
    try: 
        elem = cfg
        for part in path.split("."):
            elem = elem[part]

        if isinstance(elem, dict):
            logger.debug(f"Getting config dict '{path}' = \n{pprint.pformat(elem)}")
        else:
            logger.debug(f"Getting config element '{path}' = {elem}")
        return elem
    
    except Exception as e:
        logger.error(f"Error getting config element '{path}': {e}")
        raise e

def get_xy_scaled(path):
    try:
        anchor = get_config_element(path + ".anchor")
        if not anchor:
            anchor = "center"
        x_res = get_config_element("resolution.x")
        y_res = get_config_element("resolution.y")
        x     = get_config_element(path + ".x")
        y     = get_config_element(path + ".y")

        scale = y_res / 1080
        x_scaled = x * scale
        y_scaled = y * scale
        base_width = 1920 * scale

        if x_res > base_width: # widescreen detected
            extra = x_res - base_width
            center_offset = extra / 2

            if anchor == "left":
                x_scaled = x_scaled
            elif anchor == "right":
                x_scaled = x_scaled + center_offset * 2
            elif anchor == "center":
                x_scaled = x_scaled + center_offset

            logger.debug(f"Widescreen scaling: '{path}' -> ({int(x_scaled)}, {int(y_scaled)}), bound={anchor}")
            return int(x_scaled), int(y_scaled)

        else: # normal 16:9 scaling
            logger.debug(f"16:9 scaling: '{path}' -> ({int(x_scaled)}, {int(y_scaled)})")
            return int(x_scaled), int(y_scaled)

    except Exception as e:
        logger.error(f"Error getting scaled coordinates for '{path}': {e}")
        raise
