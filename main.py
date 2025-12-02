from gui import PoEGui
import config
import logger

class MainApp:
    def __init__(self):
        logger.info("Starting PoE Script Manager")
        config.load_config()
        self.gui = PoEGui()

    def run(self):
        self.gui.run()


if __name__ == "__main__":
    app = MainApp()
    app.run()
