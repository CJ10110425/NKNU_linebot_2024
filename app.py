
from engine import PluginEngine
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
from usecase import LinebotUtility

import warnings
from linebot import LineBotSdkDeprecatedIn30
warnings.filterwarnings("ignore", category=LineBotSdkDeprecatedIn30)

app = Flask(__name__)


line_bot_info = LinebotUtility.setup_linebot()
# Channel Access Token
line_bot_api = LineBotApi(line_bot_info["LINE_BOT_CHANNEL_ACCESS_TOKEN"])
# Channel Secret
handler = WebhookHandler(line_bot_info["LINE_BOT_CHANNEL_SECRET"])

# Webhook 接收來自 Line 平台的訊息
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # 取得 request body
    body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)

    # 處理 webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    pulgin = PluginEngine(line_bot_api, event)
    pulgin.run()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
