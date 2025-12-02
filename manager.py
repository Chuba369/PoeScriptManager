import os
import sys
import threading
import logger
import importlib.util

# -------------------------------
# Setup paths
# -------------------------------
# Get the folder where the EXE actually lives
if getattr(sys, "frozen", False):
    # Running as PyInstaller EXE
    BASE_PATH = os.path.dirname(sys.executable)
else:
    # Running as normal Python script
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

SCRIPTS_DIR = os.path.join(BASE_PATH, "scripts")

# Add scripts folder to sys.path (optional, but keeps old imports working)
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

# -------------------------------
# Load script files dynamically
# -------------------------------
if not os.path.exists(SCRIPTS_DIR):
    logger.error(f"Scripts folder not found: {SCRIPTS_DIR}")
    script_files = []
else:
    script_files = [
        f[:-3] for f in os.listdir(SCRIPTS_DIR)
        if f.endswith(".py") and f != "__init__.py" and "inactive" not in f.lower()
    ]

script_modules = {}

for name in script_files:
    module_path = os.path.join(SCRIPTS_DIR, f"{name}.py")
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        script_modules[name] = module
    except Exception as e:
        logger.error(f"Failed to load script {name}: {e}")

# -------------------------------
# Script runner
# -------------------------------
script_thread = None
current_module = None

def start_script(name):
    global script_thread, current_module

    if is_script_running():
        logger.warn(f"Cannot start '{name}', a script is already running!")
        return

    current_module = script_modules.get(name)
    if current_module:
        if not hasattr(current_module, "start"):
            logger.error(f"Script '{name}' has no start() function!")
            current_module = None
            return

        script_thread = threading.Thread(target=current_module.start, daemon=True)
        logger.info(f"Started script: {name}")
        script_thread.start()
    else:
        logger.error(f"Script '{name}' not found!")

def stop_script():
    global script_thread, current_module

    if not is_script_running():
        logger.warn("No script is currently running.")
        return

    if current_module and hasattr(current_module, "stop"):
        try:
            current_module.stop()
            if script_thread:
                script_thread.join()
            logger.info("Stopped script")
        except Exception as e:
            logger.error(f"Error while stopping script: {e}")
    else:
        logger.warn("Current script has no stop() function.")

    current_module = None
    script_thread = None

def is_script_running():
    return script_thread is not None and script_thread.is_alive()
