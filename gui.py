import tkinter as tk
from tkinter import scrolledtext
import keyboard

import logger
import config
import manager
import config_editor

class PoEGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PoE Script Manager")
        self.root.geometry("1600x900")

        self._setup_frames()
        self._setup_control_scripts()
        self._setup_info()
        self._setup_control_buttons()
        self._setup_log()
        self._setup_hotkeys()

        # Handle graceful exit
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _setup_frames(self):
        self.controls_frame = tk.Frame(self.root, padx=10, pady=10)
        self.controls_frame.grid(row=0, column=0, sticky="ns")

        self.log_frame = tk.Frame(self.root, padx=10, pady=10)
        self.log_frame.grid(row=0, column=1, sticky="nsew")
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

    def _setup_control_scripts(self):
        self.script_var = tk.StringVar(value="__none__")

        tk.Label(self.controls_frame, text="Select Script:", font=("Arial", 12, "bold")).pack(anchor="w")
        for script_name in manager.script_modules:
            tk.Radiobutton(
                self.controls_frame, text=script_name, variable=self.script_var,
                value=script_name, command=self.on_script_selected
            ).pack(anchor="w", pady=2)

    def _setup_control_buttons(self):
        reload_btn = tk.Button(self.controls_frame, text="Reload Config", command=config.load_config)
        reload_btn.pack(side=tk.LEFT, padx=(0, 5))
        config_btn = tk.Button(self.controls_frame, text="Edit Config", command=self.open_config_editor)
        config_btn.pack(side=tk.LEFT, padx=(5, 0))

    def _setup_info(self):
        info_frame = tk.LabelFrame(self.controls_frame, text="Info", padx=5, pady=5)
        info_frame.pack(fill="x", pady=(10, 5))

        tk.Label(info_frame, text="Select script from list above").pack(anchor="w")
        tk.Label(info_frame, text="Use hotkeys to manage scripts").pack(anchor="w")
        tk.Label(info_frame, text="1 - Start selected script").pack(anchor="w")
        tk.Label(info_frame, text="4 - Stop script").pack(anchor="w")
        tk.Label(info_frame, text="5 - Clear selection").pack(anchor="w")
        tk.Label(info_frame, text="Reload config after editing .json").pack(anchor="w")

    def _setup_log(self):
        tk.Label(self.log_frame, text="Log:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.log_text = tk.scrolledtext.ScrolledText(self.log_frame, width=70, height=25, state="disabled")
        self.log_text.pack(fill="both", expand=True)

        # Link the log widget
        logger.set_log_widget(self.log_text)
        self.root.after(100, lambda: logger.update_log(self.root))

    def _setup_hotkeys(self):
        keyboard.add_hotkey('1', lambda: manager.start_script(self.script_var.get()))
        keyboard.add_hotkey('4', manager.stop_script)
        keyboard.add_hotkey('5', self.clear_selection)

    # --- GUI callbacks ---
    def on_script_selected(self):
        selected = self.script_var.get()
        logger.info(f"Selected script: {selected}")

    def clear_selection(self):
        self.script_var.set("__none__")
        logger.info("Script selection cleared")

    def on_close(self):
        manager.stop_script()
        keyboard.unhook_all_hotkeys()
        self.root.destroy()

    def open_config_editor(self):
        editable_fields = {
            "log.level": str,
            "poeninja.league.name": str,
            "poeninja.scarab.chaos_value": int,
            "delay.value": int,
            "resolution.x": int,
            "resolution.y": int,
            "character.inventory.reserved": list,
            "maps.mods.avoid": list,
            "maps.mods.rarity": int,
            "maps.mods.quantity": int,
            "maps.mods.packsize": int,
            "maps.mods.currency": int,
            "maps.mods.scarabs": int,
            "maps.mods.maps": int,
            "maps.mods.sum_currency_scarab": int,
            "maps.mods.sum_currency_scarab_map": int,
            "items.name.desired.group1": list,
            "items.name.desired.group2": list
        }
        config_editor.ConfigEditor(self.root, editable_fields)

    # --- Run GUI ---
    def run(self):
        self.root.mainloop()
