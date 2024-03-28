import json
import os

from linebot.models import QuickReplyButton, MessageAction

from engine.engine_contract import PluginContract
from plugins.linebot_basic_function import LineBotBasicFunction
from .utils import SchoolBus, Bus


class Plugin(PluginContract):
    def __init__(self, line_bot_api, event) -> None:
        super().__init__(line_bot_api, event)
        self.SchoolBus = SchoolBus()
        self.Bus = Bus()
        with open(os.path.abspath(os.path.dirname(__file__)) + "/utils/flex_message.json", encoding="utf-8") as f:
            self.flex_message_json = json.loads(f.read())

    def run(self) -> None:

        # TODO 檢測距離上次 call refresh 是否超過24hr 超過就 call refresh

        linebot_basic_function = LineBotBasicFunction(self.line_bot_api, self.event)
        if "ʕ •ᴥ•ʔ 和平->燕巢" in self.event.message.text:
            match self.event.message.text:
                case "ʕ •ᴥ•ʔ 和平->燕巢":
                    # TODO show quick actions button to let use choose display next bus or all bus schedule
                    # TODO 讓使用者選擇特定時間的最近班次
                    linebot_basic_function.reply_quick_actions("ʕ •ᴥ•ʔ 和平->燕巢 校車查詢系統", [
                        QuickReplyButton(
                            action=MessageAction(label="最近的班次", text="ʕ •ᴥ•ʔ 和平->燕巢 校車查詢 最近的班次")),
                        QuickReplyButton(
                            action=MessageAction(label="特定時間最近的班次",
                                                 text="ʕ •ᴥ•ʔ 和平->燕巢 校車查詢 特定時間最近的班次")),
                        QuickReplyButton(
                            action=MessageAction(label="全部班次", text="ʕ •ᴥ•ʔ 和平->燕巢 校車查詢 全部班次"))
                    ])
                    return
                case "ʕ •ᴥ•ʔ 和平->燕巢 校車查詢 最近的班次":
                    nearest_school_bus = self.SchoolBus.get_next_school_bus_schedule_heping_2_yanchao()
                    # TODO flex message reply
                    if nearest_school_bus is None:
                        nearest_school_bus = "已經沒車了"
                    linebot_basic_function.reply_message(str(nearest_school_bus))
                    return
                case "ʕ •ᴥ•ʔ 和平->燕巢 校車查詢 特定時間最近的班次":
                    linebot_basic_function.reply_flex_message("Time Picker",
                                                              self.flex_message_json['next_school_bus_time_picker'])
                    pass
                case "ʕ •ᴥ•ʔ 和平->燕巢 校車查詢 全部班次":
                    all_bus = self.SchoolBus.get_all_school_bus_schedule_heping_2_yanchao()
                    # TODO flex message reply
                    linebot_basic_function.reply_message(str(all_bus))
                    return
        elif "ʕ •ᴥ•ʔ 燕巢->和平" in self.event.message.text:
            match self.event.message.text:
                case "ʕ •ᴥ•ʔ 燕巢->和平":
                    # TODO show quick actions button to let use choose display next bus or all bus schedule
                    # TODO 讓使用者選擇特定時間的最近班次
                    linebot_basic_function.reply_quick_actions("ʕ •ᴥ•ʔ 燕巢->和平 校車查詢系統", [
                        QuickReplyButton(
                            action=MessageAction(label="最近的班次", text="ʕ •ᴥ•ʔ 燕巢->和平 校車查詢 最近的班次")),
                        QuickReplyButton(
                            action=MessageAction(label="特定時間最近的班次",
                                                 text="ʕ •ᴥ•ʔ 燕巢->和平 校車查詢 特定時間最近的班次")),
                        QuickReplyButton(
                            action=MessageAction(label="全部班次", text="ʕ •ᴥ•ʔ 燕巢->和平 校車查詢 全部班次"))])
                    return
                case "ʕ •ᴥ•ʔ 燕巢->和平 校車查詢 最近的班次":
                    nearest_school_bus = self.SchoolBus.get_next_school_bus_schedule_yanchao_2_heping()
                    # TODO flex message reply
                    if nearest_school_bus is None:
                        nearest_school_bus = "已經沒車了"
                    linebot_basic_function.reply_message(str(nearest_school_bus))
                    return
                case "ʕ •ᴥ•ʔ 燕巢->和平 校車查詢 全部班次":
                    all_bus = self.SchoolBus.get_all_school_bus_schedule_yanchao_2_heping()
                    # TODO flex message reply
                    linebot_basic_function.reply_message(str(all_bus))
                    return
        elif "ʕ •ᴥ•ʔ 燕巢公車" in self.event.message.text:

            if "最近的班次" in self.event.message.text and "我在：" in self.event.message.text:
                user_station = self.event.message.text.split("：")[1]
                schedules = self.Bus.get_next_bus(user_station, self.event.message.text.split(" ")[4])

                for schedule_type in schedules.keys():
                    time_list = list(list(schedules[schedule_type])[0])
                    flex_message = json.loads(json.dumps(self.flex_message_json["bus_time_line"]))
                    flex_message["header"]["contents"][0]["contents"][1]["text"] = self.Bus.all_station_Zuoying2YanChao[0]
                    flex_message["header"]["contents"][1]["contents"][1]["text"] = self.Bus.all_station_Zuoying2YanChao[-1]
                    for i in range(len(self.Bus.all_station_Zuoying2YanChao)):
                        station_name = self.Bus.all_station_Zuoying2YanChao[i]
                        time = time_list[i].value

                        stop = json.loads(json.dumps(self.flex_message_json["bus_time_line_stop"]))
                        stop["contents"][0]["text"] = time.strftime("%H:%M")
                        stop["contents"][2]["text"] = station_name
                        flex_message["body"]["contents"].append(stop)
                        if i != len(self.Bus.all_station_Zuoying2YanChao) - 1:
                            flex_message["body"]["contents"].append(self.flex_message_json["bus_time_line_deco"])
                    print(flex_message)
                    # FIXME use push_message instead 因為還要發寒假/周末
                    linebot_basic_function.reply_flex_message("aaaaa", flex_message)
                return

            match self.event.message.text:
                case "ʕ •ᴥ•ʔ 燕巢公車":
                    linebot_basic_function.reply_quick_actions("ʕ •ᴥ•ʔ 燕巢公車 查詢系統", [
                        QuickReplyButton(
                            action=MessageAction(label="最近的班次", text="ʕ •ᴥ•ʔ 燕巢公車 最近的班次")),
                        QuickReplyButton(
                            action=MessageAction(label="特定時間最近的班次",
                                                 text="ʕ •ᴥ•ʔ 燕巢公車 特定時間最近的班次")),
                        QuickReplyButton(
                            action=MessageAction(label="全部班次", text="ʕ •ᴥ•ʔ 燕巢公車 全部班次"))
                    ])
                    return
                case "ʕ •ᴥ•ʔ 燕巢公車 最近的班次":
                    linebot_basic_function.reply_quick_actions("ʕ •ᴥ•ʔ 燕巢公車 最近的班次 查詢系統", [
                        QuickReplyButton(
                            action=MessageAction(label="往高師大燕巢校區",
                                                 text="ʕ •ᴥ•ʔ 燕巢公車 最近的班次 往高師大燕巢校區")),
                        QuickReplyButton(
                            action=MessageAction(label="往左營高鐵站",
                                                 text="ʕ •ᴥ•ʔ 燕巢公車 最近的班次 往左營高鐵站"))])
                    return
                case "ʕ •ᴥ•ʔ 燕巢公車 最近的班次 往高師大燕巢校區":
                    linebot_basic_function.push_flex_message(alt_text="請選擇你所在的站點",
                                                             contents=self.Bus.generate_station_selector_flex_message(
                                                                 self.Bus.all_station_Zuoying2YanChao[:9]))
                    linebot_basic_function.push_flex_message(alt_text="請選擇你所在的站點",
                                                             contents=self.Bus.generate_station_selector_flex_message(
                                                                 self.Bus.all_station_Zuoying2YanChao[9:]))
                    linebot_basic_function.push_message("請選擇你所在的站點")
                    return
                case "ʕ •ᴥ•ʔ 燕巢公車 最近的班次 往左營高鐵站":
                    return
                case "ʕ •ᴥ•ʔ 燕巢公車 特定時間最近的班次":
                    linebot_basic_function.reply_quick_actions("ʕ •ᴥ•ʔ 燕巢公車 特定時間最近的班次 查詢系統", [
                        QuickReplyButton(
                            action=MessageAction(label="往高師大燕巢校區",
                                                 text="ʕ •ᴥ•ʔ 燕巢公車 特定時間最近的班次 往高師大燕巢校區")),
                        QuickReplyButton(
                            action=MessageAction(label="往左營高鐵站",
                                                 text="ʕ •ᴥ•ʔ 燕巢公車 特定時間最近的班次 往左營高鐵站"))])
                    return
                case "ʕ •ᴥ•ʔ 燕巢公車 全部班次":
                    linebot_basic_function.reply_quick_actions("ʕ •ᴥ•ʔ 燕巢公車 全部班次 查詢系統", [
                        QuickReplyButton(
                            action=MessageAction(label="往高師大燕巢校區",
                                                 text="ʕ •ᴥ•ʔ 燕巢公車 全部班次 往高師大燕巢校區")),
                        QuickReplyButton(
                            action=MessageAction(label="往左營高鐵站",
                                                 text="ʕ •ᴥ•ʔ 燕巢公車 全部班次 往左營高鐵站"))])
                    return
