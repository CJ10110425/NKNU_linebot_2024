# plugin_1/main.py
from engine.engine_contract import PluginContract

class Plugin(PluginContract):
    def __init__(self, line_bot_api, event) -> None:
        super().__init__(line_bot_api, event) 
    def run(self) -> None:
        print("Plugin 1 is running!")
