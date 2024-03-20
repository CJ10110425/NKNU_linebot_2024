# plugin_2/main.py

from engine.engine_contract import PluginContract
from linebot.models import TextSendMessage


class Plugin(PluginContract):
    def __init__(self, line_bot_api, event) -> None:
        super().__init__(line_bot_api, event)  # 调用父类构造器

    def run(self) -> None:
        # 现在可以使用 self.line_bot_api 和 self.event 来回复消息了
        message = self.event.message.text
        user_id = self.event.source.user_id
        if message == "幹你娘":
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(text=user_id + message)
            )

        print("Plugin 4 is running!")
