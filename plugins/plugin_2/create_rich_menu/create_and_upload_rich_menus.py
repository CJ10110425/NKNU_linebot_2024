import json
from linebot import LineBotApi
from linebot.models import RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, MessageAction
import sys
import os
'''
    FIXME: 靠杯，我想用 LinebotUtility 但是它鎖在外面，因為把它包起來了，所以先讓sys位置退到根目錄～～ 我不知道要怎麼解
'''
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', '..')))
from usecase import LinebotUtility


# 創建 Rich Menu
def create_rich_menu(data):
    rich_menu = RichMenu(
        size=RichMenuSize(**data["size"]),
        selected=data["selected"],
        name=data["name"],
        chat_bar_text=data["chatBarText"],
        areas=[RichMenuArea(bounds=RichMenuBounds(
            **area["bounds"]), action=MessageAction(**area["action"])) for area in data["areas"]]
    )
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu)
    return rich_menu_id


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

    with open("plugins/plugin_2/src/rich_menus_name_id.json", "w", encoding="utf-8") as json_file:
        json.dump(rich_menus_name_id, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # 設置 LineBot 的存取權杖
    line_bot_api = LineBotApi(LinebotUtility.setup_linebot()[
                                "LINE_BOT_CHANNEL_ACCESS_TOKEN"])

    # 讀取 JSON 檔案
    with open("plugins/plugin_2/src/rich_menus.json", "r", encoding="utf-8") as f:
        rich_menus_data = json.load(f)
    main()
