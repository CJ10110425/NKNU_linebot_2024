# linebot-_basic_function.py 製作 linebot 擁有基本的功能
# 主要功能為:
# 1. 回覆使用者訊息
# 2. 主動推播訊息

import json

from linebot.models import (
    TextSendMessage,
    ImageSendMessage,
    QuickReply,
    FlexSendMessage,
    FlexContainer,
    DatetimePickerAction
)


class LineBotBasicFunction():
    def __init__(self, line_bot_api, event):
        self.line_bot_api = line_bot_api
        self.event = event
        self.user_id = event.source.user_id
        self.message = event.message.text

    # 讀取 image.json的內容回傳一個 dict
    def __read_image_json(self) -> dict:
        with open("plugins/plugin_1/src/image.json", "r", encoding="utf-8") as image_file:
            image_json = image_file.read()
            image_dict = json.loads(image_json)
        return image_dict

    def get_msg(self):
        return self.message

    def get_user_id(self):
        return self.user_id

    def reply_message(self, message=str):
        self.line_bot_api.reply_message(
            self.event.reply_token,
            TextSendMessage(text=message)
        )

    def reply_image_message(self, image_url=str):
        image_dict = self.__read_image_json()
        self.line_bot_api.reply_message(
            self.event.reply_token,
            ImageSendMessage(
                original_content_url=image_url,
                preview_image_url=image_dict["loading_image"]
            )
        )

    def reply_quick_actions(self, text: str = "", items: list = None):
        if items is None:
            raise Exception("No items provided")
        self.line_bot_api.reply_message(
            self.event.reply_token,
            TextSendMessage(
                text=text,
                quick_reply=QuickReply(
                    items=items
                )
            )
        )

    def reply_flex_message(self, alt_text: str = "", contents=None):
        if contents is None:
            raise Exception("No contents provided")
        self.line_bot_api.reply_message(
            self.event.reply_token,
            FlexSendMessage(
                alt_text=alt_text,
                contents=contents
            )
        )

        # 使用者可以輸入 user_id 來推播訊息或是直接使用預設的 self_user_id 推播訊息

    def push_message(self, message=str, user_id=None):
        if user_id:
            self.line_bot_api.push_message(
                user_id, TextSendMessage(text=message))
        else:
            self.line_bot_api.push_message(
                self.user_id, TextSendMessage(text=message))

    def link_rich_menu_to_user(self, rich_menu_id):
        '''
            輸入 rich_menu_id 來連結 rich_menu_id 到 user_id 上
        '''
        self.line_bot_api.link_rich_menu_to_user(self.user_id, rich_menu_id)
