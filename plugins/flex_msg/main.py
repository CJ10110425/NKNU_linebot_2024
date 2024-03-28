
from engine.engine_contract import PluginContract
import os
import logging
import json
from linebot.models import FlexSendMessage
import linebot
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class Plugin(PluginContract):
    def __init__(self, line_bot_api, event) -> None:
        super().__init__(line_bot_api, event)

    def run(self) -> None:
        script_dir = os.path.dirname(__file__)
        folder_name = os.path.basename(script_dir)
        logger.info(f"{folder_name} is running!")
    
    @staticmethod
    def create_flex_msg(template_count, titles, admin_infos, pub_dates, course_infos, link_urls, image_urls=None):
        if image_urls is None:
            image_urls = [
                "https://cdn.discordapp.com/attachments/1222446430258466877/1222446656893616249/image.png?ex=66163f2a&is=6603ca2a&hm=af3159e8df7baf893c3bb2329ef1bce1b21360bd98e78a5f962e223b460fa9d1&",
                "https://cdn.discordapp.com/attachments/1222446430258466877/1222447079931121714/image.png?ex=66163f8f&is=6603ca8f&hm=315165886f56bb0fb406fee96bb79ec99d23bf35cc1c30f55e67cd13ac94e5ec&"
            ]
        
        templates = []
        for i in range(template_count):
            with open(os.path.dirname(__file__)+'/src/flex_msg.json', 'r', encoding='utf-8') as f:
                json_template_str = f.read()
            json_template = json.loads(json_template_str)
            
            json_template['hero']['url'] = image_urls[i % len(image_urls)]  
            json_template['body']['contents'][0]['text'] = titles[i]
            json_template['body']['contents'][1]['text'] = admin_infos[i]
            json_template['body']['contents'][2]['text'] = pub_dates[i]
            json_template['body']['contents'][3]['text'] = course_infos[i]
            json_template['body']['contents'][4]['action']['uri'] = link_urls[i]     

            if not templates:
                templates.append({
                    "type": "carousel",
                    "contents": []
                })
            templates[0]['contents'].append(json_template)

        msg = FlexSendMessage(alt_text='ʕ •ᴥ•ʔ', contents=templates[0])
        return msg
    
