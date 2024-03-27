# engine_contract.py
from linebot.models import TextSendMessage

class PluginContract:
    def __init__(self, line_bot_api, event):
        self.line_bot_api = line_bot_api
        self.event = event

    def run(self):
        raise NotImplementedError("Plugins must implement the 'run' method.")
