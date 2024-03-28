
from engine.engine_contract import PluginContract
from linebot.models import TextSendMessage
from plugins.linebot_basic_function import LineBotBasicFunction
import os
import logging
from datetime import datetime
import json
from plugins.flex_msg import create_flex_msg
from .rss_scraper import RssScraper
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class Plugin(PluginContract):
    def __init__(self, line_bot_api, event) -> None:
        super().__init__(line_bot_api, event)  # 调用父类构造器

    def __get_school_news(self) -> dict:
        '''
            因為 template 最多只能傳送十三個樣板所以只會找到最新的資料
        '''
        news_data = {
            "template_count": 0,
            "titles": [],
            "description": [],
            "pub_dates": [],
            "category": [],
            "link": []
        }
        with open(os.path.dirname(__file__)+"/src/school_news_info.json") as news_info:
            news_json = json.load(news_info)
        # 從 school_news_info.json 找出最新的 13 個消息
        sorted_news = sorted(news_json, key=lambda x: datetime.strptime(
            x['pubDate'], "%Y-%m-%d %H:%M:%S"), reverse=True)
        for event in sorted_news[:12]:
            news_data['template_count'] += 1
            news_data['titles'].append(event['title'])
            news_data['description'].append(event['description'])
            news_data['pub_dates'].append(event['pubDate'])
            news_data['category'].append(event['category'])
            news_data['link'].append(event['link'])

        return news_data

    def run(self) -> None:
        linebot = LineBotBasicFunction(self.line_bot_api, self.event)
        if linebot.get_msg() == "ʕ •ᴥ•ʔ 最新消息":
            news_data = self.__get_school_news()
            msg = create_flex_msg(*news_data.values())
            linebot.reply_flex_msg(msg)
            updated_school_news = RssScraper()

        script_dir = os.path.dirname(__file__)
        folder_name = os.path.basename(script_dir)
        logger.info(f"{folder_name} is running!")
