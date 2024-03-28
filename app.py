import warnings

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot import LineBotSdkDeprecatedIn30
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, PostbackEvent
)

from engine import PluginEngine
from usecase import LinebotUtility

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    pulgin = PluginEngine(line_bot_api, event, register_plugins)
    pulgin.run()


@handler.add(PostbackEvent)
def handle_postback(event):
    # TODO 做成plugin架構
    print(event.postback.data)
    print(event.postback.params)


if __name__ == "__main__":
    # 回傳成功註冊的 plugins
    register_plugins = PluginEngine.register_plugins()
    app.run(host='0.0.0.0', port=8080)
