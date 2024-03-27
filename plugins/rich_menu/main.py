# plugin_2/main.py

from engine.engine_contract import PluginContract
from plugins.linebot_basic_function import LineBotBasicFunction
import json
import os
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class Plugin(PluginContract):
    def __init__(self, line_bot_api, event) -> None:
        super().__init__(line_bot_api, event)

    def run(self) -> None:
        with (open(os.path.dirname(__file__)+"/src/rich_menus_name_id.json", "r", encoding="utf-8")) as rich_menu_file:
            rich_menu_json = rich_menu_file.read()
            rich_menu = json.loads(rich_menu_json)
        linebot = LineBotBasicFunction(self.line_bot_api, self.event)
        
        match linebot.get_msg():
            case "ʕ •ᴥ•ʔ 校/公車時刻表":
                linebot.link_rich_menu_to_user(rich_menu["feature_1_menu"])
            case "ʕ •ᴥ•ʔ 校務專區":
                linebot.link_rich_menu_to_user(rich_menu["feature_2_menu"])
            case "ʕ •ᴥ•ʔ 校園地圖":
                linebot.link_rich_menu_to_user(rich_menu["feature_4_menu"])
            case "ʕ •ᴥ•ʔ 校內電話":
                linebot.link_rich_menu_to_user(rich_menu["feature_2.1_menu"])
            case "ʕ •ᴥ•ʔ 常用連結":
                linebot.link_rich_menu_to_user(rich_menu["feature_2.4_menu"])
            case "ʕ •ᴥ•ʔ 回到主選單":
                linebot.link_rich_menu_to_user(rich_menu["home_view"])

        script_dir = os.path.dirname(__file__)
        folder_name = os.path.basename(script_dir)
        logger.info(f"{folder_name} is running!")
