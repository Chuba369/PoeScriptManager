import win32gui
import win32con
import re
import time

# Activate window with expected title  
def activate_window(expected_title):
    hwnd = win32gui.GetForegroundWindow()
    current_title = win32gui.GetWindowText(hwnd)
    
    # Debug print
    print(f"Current active window: {current_title}")
    
    if current_title != expected_title:
        # Find window with exact fallback title
        target_hwnd = win32gui.FindWindow(None, expected_title)
        if target_hwnd:
            # Restore if minimized
            win32gui.ShowWindow(target_hwnd, win32con.SW_RESTORE)
            # Bring to foreground
            win32gui.SetForegroundWindow(target_hwnd)
            print(f"Activated window: {expected_title}")
        else:
            print(f"Window with title '{expected_title}' not found.")

def parse_map_string(map_string):
    lines = map_string.splitlines()
    map_info = {
        "quantity": None,
        "rarity": None,
        "pack_size": None,
        "more_maps": None,
        "more_scarabs": None,
        "more_currency": None,
        "modifiers": []
    }

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Skip separator lines
        m = re.match(r"--------", line)
        if m:
            continue        

        # Quantity
        m = re.match(r"Item Quantity: \+(\d+)%.*", line)
        if m:
            map_info["quantity"] = int(m.group(1))
            continue

        # Rarity
        m = re.match(r"Item Rarity: \+(\d+)%.*", line)
        if m:
            map_info["rarity"] = int(m.group(1))
            continue

        # Monster Pack Size
        m = re.match(r"Monster Pack Size: \+(\d+)%.*", line)
        if m:
            map_info["pack_size"] = int(m.group(1))
            continue

        # More Maps
        m = re.match(r"More Maps: \+(\d+)%.*", line)
        if m:
            map_info["more_maps"] = int(m.group(1))
            continue

        # More Scarabs
        m = re.match(r"More Scarabs: \+(\d+)%.*", line)
        if m:
            map_info["more_scarabs"] = int(m.group(1))
            continue

        # More Currency
        m = re.match(r"More Currency: \+(\d+)%.*", line)
        if m:
            map_info["more_currency"] = int(m.group(1))
            continue

        # Anything else is treated as a modifier
        map_info["modifiers"].append(line)

    return map_info

def has_bad_map_mods(map_mods, bad_mods):
    matches = [
        mod for mod in map_mods
        if any(bad.lower() in mod.lower() for bad in bad_mods)
    ]
    return bool(matches), matches

def parse_scarab_string(scarab_string):
    lines = scarab_string.splitlines()
    stack_size = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue      

        m = re.match(r"Stack Size: (\d+)/20", line)
        if m:
            stack_size = int(m.group(1))
            return stack_size

def item_match_mods(text, mods):    
    # If the group is empty (or all ignored), consider it automatically satisfied
    if not mods:
        return True
    
    for mod in mods:
        pattern = mod.get("pattern")
        min_val = mod.get("min_value")
        max_val = mod.get("max_value")
        
        match = re.search(pattern, text)
        if match:
            value = int(match.group(1))
            if (min_val is None or value >= min_val) and (max_val is None or value <= max_val):
                return True
    
    return False

def item_match_name(text, group1, group2):
    text_lower = text.lower()

    if group1: 
        if not any(word.lower() in text_lower for word in group1):
            return False

    if group2:
        if not any(word.lower() in text_lower for word in group2):
            return False

    return True

def sleep(ms: int):
    time.sleep(ms / 1000)

