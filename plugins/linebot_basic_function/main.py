# plugin_1/main.py
from engine.engine_contract import PluginContract
import os
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class Plugin(PluginContract):
    def __init__(self, line_bot_api, event) -> None:
        super().__init__(line_bot_api, event)

    def run(self) -> None:
        script_dir = os.path.dirname(__file__)
        folder_name = os.path.basename(script_dir)
        logger.info(f"{folder_name} is running!")
