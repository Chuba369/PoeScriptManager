import ast
import tkinter as tk
from tkinter import messagebox
import json

import config
import logger

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

class ConfigEditor:
    def __init__(self, master, editable_fields):
        self.master = master
        self.editable_fields = editable_fields
        self.window = tk.Toplevel(master)
        self.window.title("Config Editor")

        self.window.geometry("1366x768")
        self.window.resizable(True, True)

        self.entries = {}

        with open("config.json", "r") as f:
            self.config_data = json.load(f)

        row = 0
        for field_path, field_type in editable_fields.items():
            tk.Label(self.window, text=field_path).grid(row=row, column=0, sticky="w", padx=5, pady=5)
            
            value = self.get_nested_value(field_path, self.config_data)

            # if the field is a list, format it with double quotes for strings only
            if self.editable_fields[field_path] == list and isinstance(value, list):
                value = "[" + ", ".join(f'"{s}"' if isinstance(s, str) else str(s) for s in value) + "]"

            entry = tk.Entry(self.window, width=150)  
            entry.insert(0, str(value))
            entry.grid(row=row, column=1, padx=5, pady=5)
            self.entries[field_path] = entry

            comment = self.find_closest_comment(field_path)
            if comment:
                ToolTip(entry, comment)

            row += 1

        tk.Button(self.window, text="Cancel", command=self.window.destroy).grid(row=row, column=0, pady=10)
        tk.Button(self.window, text="Save & Close", command=self.save).grid(row=row, column=1, pady=10)

    def get_nested_value(self, path, data):
        keys = path.split(".")
        for key in keys:
            data = data[key]
        return data

    def set_nested_value(self, path, data, value):
        keys = path.split(".")
        for key in keys[:-1]:
            data = data[key]
        data[keys[-1]] = value

    def find_closest_comment(self, path):
        keys = path.split(".")
        for i in range(len(keys), 0, -1):
            try:
                subdict = self.get_nested_value(".".join(keys[:i]), self.config_data)
                if isinstance(subdict, dict) and "comment" in subdict:
                    return subdict["comment"]
            except KeyError:
                continue
        return None
    
    def save(self):
        for field, entry in self.entries.items():
            value = entry.get()

            if self.editable_fields[field] == int:
                if value == "None" or value.lower() == "null" or value == "":
                    value = None
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        messagebox.showerror("Invalid Input", f"Field '{field}' requires an integer value or None.")
                        return
                    
            elif self.editable_fields[field] == list:
                if value == "None" or value.lower() == "null" or value == "":
                    value = []
                else:
                    try:
                        parsed_value = ast.literal_eval(value)
                        if not isinstance(parsed_value, list):
                            raise ValueError
                        value = parsed_value
                    except (ValueError, SyntaxError):
                        messagebox.showerror("Invalid Input", f"Field '{field}' requires a valid list.")
                        return           

            self.set_nested_value(field, self.config_data, value)

        with open("config.json", "w") as f:
            json.dump(self.config_data, f, indent=4)

        config.load_config()
        logger.info("Configuration saved and reloaded")
        self.window.destroy()