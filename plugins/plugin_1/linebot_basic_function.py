# linebot-_basic_function.py 製作 linebot 擁有基本的功能
# 主要功能為:
# 1. 回覆使用者訊息
# 2. 主動推播訊息


from linebot.models import (
    TextSendMessage
)


class LineBotBasicFunction():
    def __init__(self, line_bot_api, event):
        self.line_bot_api = line_bot_api
        self.event = event
        self.user_id = event.source.user_id
        self.message = event.message.text

    def get_msg(self):
        return self.message

    def get_user_id(self):
        return self.user_id

    def reply_message(self, message=str):
        self.line_bot_api.reply_message(
            self.event.reply_token,
            TextSendMessage(text=message)
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
        self.line_bot_api.link_rich_menu_to_user(self.user_id, rich_menu_id)
