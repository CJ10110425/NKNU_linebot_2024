
from engine.engine_contract import PluginContract
from linebot.models import TextSendMessage


class Plugin(PluginContract):
    def __init__(self, line_bot_api, event) -> None:
        super().__init__(line_bot_api, event)  # 调用父类构造器

    def run(self) -> None:

        print("plugin_default is running!")
