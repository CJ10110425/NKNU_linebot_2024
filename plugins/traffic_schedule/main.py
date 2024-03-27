from linebot.models import QuickReplyButton, MessageAction

from engine.engine_contract import PluginContract
from plugins.linebot_basic_function import LineBotBasicFunction
from .utils import SchoolBus


class Plugin(PluginContract):
    def __init__(self, line_bot_api, event) -> None:
        super().__init__(line_bot_api, event)
        self.SchoolBus = SchoolBus()

    def run(self) -> None:

        # TODO 檢測距離上次 call refresh 是否超過24hr 超過就 call refresh

        linebot_basic_function = LineBotBasicFunction(self.line_bot_api, self.event)
        match self.event.message.text:
            case "ʕ •ᴥ•ʔ 和平->燕巢":
                # TODO show quick actions button to let use choose display next bus or all bus schedule
                linebot_basic_function.reply_quick_actions("ʕ •ᴥ•ʔ 和平->燕巢 請到手機上使用", [
                    QuickReplyButton(
                        action=MessageAction(label="最近的班次", text="ʕ •ᴥ•ʔ 和平->燕巢 校車查詢 最近的班次")),
                    QuickReplyButton(
                        action=MessageAction(label="全部班次", text="ʕ •ᴥ•ʔ 和平->燕巢 校車查詢 全部班次"))
                ])
            case "ʕ •ᴥ•ʔ 和平->燕巢 校車查詢 最近的班次":
                nearest_school_bus = self.SchoolBus.get_next_school_bus_schedule_heping_2_yanchao()
                # TODO flex message reply
                if nearest_school_bus is None:
                    nearest_school_bus = "已經沒車了"
                linebot_basic_function.reply_message(nearest_school_bus)
            case "ʕ •ᴥ•ʔ 和平->燕巢 校車查詢 全部班次":
                all_bus = self.SchoolBus.get_all_school_bus_schedule_heping_2_yanchao()
                # TODO flex message reply
                linebot_basic_function.reply_message(str(all_bus))
            case "ʕ •ᴥ•ʔ 燕巢->和平":
                # TODO show quick actions button to let use choose display next bus or all bus schedule
                linebot_basic_function.reply_quick_actions("ʕ •ᴥ•ʔ 燕巢->和平 請到手機上使用", [
                    QuickReplyButton(
                        action=MessageAction(label="最近的班次", text="ʕ •ᴥ•ʔ 燕巢->和平 校車查詢 最近的班次")),
                    QuickReplyButton(
                        action=MessageAction(label="全部班次", text="ʕ •ᴥ•ʔ 燕巢->和平 校車查詢 全部班次"))])
            case "ʕ •ᴥ•ʔ 燕巢->和平 校車查詢 最近的班次":
                nearest_school_bus = self.SchoolBus.get_next_school_bus_schedule_yanchao_2_heping()
                # TODO flex message reply
                if nearest_school_bus is None:
                    nearest_school_bus = "已經沒車了"
                linebot_basic_function.reply_message(nearest_school_bus)
            case "ʕ •ᴥ•ʔ 燕巢->和平 校車查詢 全部班次":
                all_bus = self.SchoolBus.get_all_school_bus_schedule_yanchao_2_heping()
                # TODO flex message reply
                linebot_basic_function.reply_message(str(all_bus))
