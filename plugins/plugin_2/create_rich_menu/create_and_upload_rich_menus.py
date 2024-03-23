import json
from linebot import LineBotApi
from linebot.models import RichMenu, RichMenuSize, RichMenuBounds, MessageAction, URIAction, PostbackAction, RichMenuArea
import sys
import os
import time
'''
    FIXME: 靠杯，我想用 LinebotUtility 但是它鎖在外面，因為把它包起來了，所以先讓sys位置退到根目錄～～ 我不知道要怎麼解
'''
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', '..')))
from usecase import LinebotUtility

import warnings
from linebot import LineBotSdkDeprecatedIn30
warnings.filterwarnings("ignore", category=LineBotSdkDeprecatedIn30)


# 創建 Rich Menu
def create_rich_menu(data):
    rich_menu = RichMenu(
        size=RichMenuSize(width=data["size"]["width"], height=data["size"]["height"]),
        selected=data["selected"],
        name=data["name"],
        chat_bar_text=data["chatBarText"],
        areas=[create_rich_menu_area(area) for area in data["areas"]]
    )
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu)
    return rich_menu_id


def create_rich_menu_area(area_data):
    bounds = RichMenuBounds(**area_data["bounds"])
    action_data = area_data["action"]
    action_type = action_data.get("type", None)
    if action_type == "message":
        action = MessageAction(**action_data)
    elif action_type == "uri":
        action = URIAction(**action_data)
    elif action_type == "postback":
        action = PostbackAction(**action_data)
    else:
        action = None
    return RichMenuArea(bounds=bounds, action=action)


def upload_rich_menu_image(rich_menu_id, image_path):
    with open(image_path, 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)


def main():
    rich_menus_name_id = {}
    for data in rich_menus_data:

        rich_menu_id = create_rich_menu(data)
        print("Rich menu created with ID:", rich_menu_id)

        upload_rich_menu_image(rich_menu_id, data["img"])
        print("Rich menu image uploaded for:", data["name"])

        rich_menus_name_id[data["name"]] = rich_menu_id

        time.sleep(1)  # 等待 1 秒，避免 API 被封鎖

    with open("plugins/plugin_2/src/rich_menus_name_id.json", "w", encoding="utf-8") as json_file:
        json.dump(rich_menus_name_id, json_file, ensure_ascii=False, indent=4)
    # # 設定預設rich_menu
    # line_bot_api.set_default_rich_menu("richmenu-5f36237fd358c8828672798d910229b8")

if __name__ == "__main__":
    # 設置 LineBot 的存取權杖
    line_bot_api = LineBotApi(LinebotUtility.setup_linebot()[
        "LINE_BOT_CHANNEL_ACCESS_TOKEN"])

    # 讀取 JSON 檔案
    with open("plugins/plugin_2/src/rich_menus.json", "r", encoding="utf-8") as f:
        rich_menus_data = json.load(f)
    main()
