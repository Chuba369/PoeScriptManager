import tkinter as tk
import queue
from datetime import datetime

DEBUG = 10
INFO = 20
WARN = 30
ERROR = 40

log_queue = queue.Queue()
log_text_widget = None  # will be set from GUI
log_level = INFO # default log level - will be updated from config

def set_log_level(level_name: str):
    global log_level
    level_map = {
        "DEBUG": DEBUG,
        "INFO": INFO,
        "WARN": WARN,
        "ERROR": ERROR
    }
    log_level = level_map.get(level_name.upper(), INFO)

def debug(msg):
    log(msg, DEBUG)

def info(msg):
    log(msg, INFO)

def warn(msg):
    log(msg, WARN)

def error(msg):
    log(msg, ERROR)

def log(msg, level):
    if (level < log_level):
        return
    
    prefix = {
        DEBUG: "[DEBUG]",
        INFO: "[INFO]",
        WARN: "[WARN]",
        ERROR: "[ERROR]"
    }.get(level, "[INFO]")

    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # e.g., 15:12:34.123
    msg = f"{timestamp} {prefix} {msg}"

    log_queue.put(msg)

def update_log(root):
    if log_text_widget is None:
        return

    while not log_queue.empty():
        msg = log_queue.get_nowait()

        # Determine tag based on log level in the message
        if "[DEBUG]" in msg:
            tag = "DEBUG"
        elif "[INFO]" in msg:
            tag = "INFO"
        elif "[WARN]" in msg:
            tag = "WARN"
        elif "[ERROR]" in msg:
            tag = "ERROR"
        else:
            tag = "INFO"

        log_text_widget.configure(state="normal")
        log_text_widget.insert(tk.END, msg + "\n", tag)
        log_text_widget.see(tk.END)
        log_text_widget.configure(state="disabled")

    root.after(50, lambda: update_log(root))

def set_log_widget(widget: tk.Text):
    global log_text_widget
    log_text_widget = widget

    # Configure tags for coloring
    log_text_widget.tag_config("DEBUG", foreground="gray")
    log_text_widget.tag_config("INFO", foreground="black")
    log_text_widget.tag_config("WARN", foreground="orange")
    log_text_widget.tag_config("ERROR", foreground="red")