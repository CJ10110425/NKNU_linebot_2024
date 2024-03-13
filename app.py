from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)
import os

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.getenv("LINE_BOT_CHANNEL_ACCESS_TOKEN"))
# Channel Secret
handler = WebhookHandler(os.getenv("LINE_BOT_CHANNEL_SECRET"))

# Webhook 接收來自 Line 平台的訊息
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # 取得 request body
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 處理 webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 回覆用戶傳來的訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
