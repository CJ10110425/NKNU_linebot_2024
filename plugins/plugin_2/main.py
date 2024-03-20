# plugin_2/main.py

from engine.engine_contract import PluginContract
from linebot.models import TextSendMessage

class Plugin(PluginContract):
    def __init__(self, line_bot_api, event) -> None:
        super().__init__(line_bot_api, event)  

    def run(self) -> None:
        message = self.event.message.text
        if message == "你好":
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(text="Plugin 2 response")
            )
        print("Plugin 2 is running!")
        