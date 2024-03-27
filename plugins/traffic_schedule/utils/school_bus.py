import time
import requests
import json


class SchoolBus:
    def __init__(self):
        self.HePing2YanChao = []
        self.YanChao2HePing = []
        self.__get_heping_to_yanchao_json()
        self.__get_yanchao_to_heping_json()
        self.locations = json.dumps('./locations.json')

    def refresh_json(self):
        self.__get_heping_to_yanchao_json()
        self.__get_yanchao_to_heping_json()

    # 燕巢到和平
    def __get_yanchao_to_heping_json(self):
        res = requests.get("https://apps.nknu.edu.tw/bus_nosql/toHPJSON")
        data = json.loads(res.text)
        for item in data:
            self.YanChao2HePing.append({
                "stops": item['stops'],
                "type": item['type'],
                "note": item['note']
            })

    # 和平到燕巢
    def __get_heping_to_yanchao_json(self):
        res = requests.get("https://apps.nknu.edu.tw/bus_nosql/toYCJSON")
        data = json.loads(res.text)
        for item in data:
            self.HePing2YanChao.append({
                "stops": item['stops'],
                "type": item['type'],
                "note": item['note']
            })

    def __get_current_time(self):
        return int(time.strftime("%H", time.localtime())), int(time.strftime("%M", time.localtime()))
        # return 13, 53

    def get_next_school_bus_schedule_yanchao_2_heping(self):
        current_time_hour, current_time_min = self.__get_current_time()
        for item in self.YanChao2HePing:
            for stops in item['stops']:
                stop_time = stops['time']
                if stops['note'] == '下車':
                    continue
                if int(stop_time.split(':')[0]) == current_time_hour == int(
                        stop_time.split(':')[1]) >= current_time_min or int(
                    stop_time.split(':')[0]) > current_time_hour:
                    return item

    def get_all_school_bus_schedule_yanchao_2_heping(self):
        return self.YanChao2HePing

    def get_next_school_bus_schedule_heping_2_yanchao(self):
        current_time_hour, current_time_min = self.__get_current_time()
        for item in self.HePing2YanChao:
            for stops in item['stops']:
                stop_time = stops['time']
                if stops['note'] == '下車':
                    continue
                if int(stop_time.split(':')[0]) == current_time_hour == int(
                        stop_time.split(':')[1]) >= current_time_min or int(
                    stop_time.split(':')[0]) > current_time_hour:
                    return item

    def get_all_school_bus_schedule_heping_2_yanchao(self):
        return self.HePing2YanChao

    def get_location_info(self, location=None):
        if location is None:
            raise Exception("location is None")
        return self.locations[location]
