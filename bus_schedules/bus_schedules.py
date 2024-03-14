import openpyxl
import logging


class BusSchedules:
    def __init__(self):
        logging.info("Initializing BUS Schedules")
        try:
            wb = openpyxl.load_workbook('BUS.xlsx')
            self.Zuoying2YanChao_normal = wb["E04 高鐵左營站-高師大燕巢校區 平日時刻表"]
            self.YanChao2Zuoying_normal = wb["E04 高師大燕巢校區-高鐵左營站 平日時刻表"]
            self.Zuoying2YanChao_weekend = wb["E04 高鐵左營站-高師大燕巢校區 假日時刻表"]
            self.YanChao2Zuoying_weekend = wb["E04 高師大燕巢校區-高鐵左營站 假日時刻表"]
            self.Zuoying2YanChao_vacation = wb["E04 高鐵左營站-高師大燕巢校區 寒暑假時刻表"]
            self.YanChao2Zuoying_vacation = wb["E04 高師大燕巢校區-高鐵左營站 寒暑假時刻表"]
            logging.info("Finished")
        except Exception as e:
            logging.error("An error occurred while reading BUS.xlsx: %s", e)
        # test reading a cell
        # print(self.Zuoying2YanChao_vacation.cell(row=1, column=1).value)

    def get_next_bus(self):
        pass
