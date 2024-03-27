import os
import requests
import json


class SchoolBus:
    def __init__(self):
        self.HePing2YanChao = []
        self.YanChao2HePing = []
        self.__get_heping_to_yanchao_json()
        self.__get_yanchao_to_heping_json()
        self.locations = json.loads(
            open(os.path.abspath(os.path.dirname(__file__)) + '/locations.json', encoding="utf-8").read())

    def refresh_json(self):
        self.__get_heping_to_yanchao_json()
        self.__get_yanchao_to_heping_json()

    # 燕巢到和平
    def __get_yanchao_to_heping_json(self):
        res = requests.get("https://apps.nknu.edu.tw/bus_nosql/toHPJSON")
        if res.status_code != 200:
            raise Exception("An error occurred while trying to get yanchao_to_heping school bus data")
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
        if res.status_code != 200:
            raise Exception("An error occurred while trying to get heping_to_yanchao school bus data")
        data = json.loads(res.text)
        for item in data:
            self.HePing2YanChao.append({
                "stops": item['stops'],
                "type": item['type'],
                "note": item['note']
            })

    def __get_current_time(self):
        # return int(time.strftime("%H", time.localtime())), int(time.strftime("%M", time.localtime()))
        return 14, 6

    def get_next_school_bus_schedule_yanchao_2_heping(self):
        current_time_hour, current_time_min = self.__get_current_time()
        result = {
            "current_time": f"{current_time_hour}:{current_time_min}",
            "next_stop": None,
            "all_info": None
        }
        found = False
        for item in self.YanChao2HePing.copy():
            for stops in item['stops']:
                stop_time = stops['time']
                if stops['note'] == '下車':
                    continue
                if int(stop_time.split(':')[0]) == current_time_hour and int(
                        stop_time.split(':')[1]) >= current_time_min or int(
                    stop_time.split(':')[0]) > current_time_hour:
                    result['next_stop'] = stops.copy()
                    result['next_stop']['location'] = self.locations[stops['name']]
                    result['all_info'] = item
                    found = True
                    break
            if found:
                break
        return result

    def get_all_school_bus_schedule_yanchao_2_heping(self):
        return self.YanChao2HePing

    def get_next_school_bus_schedule_heping_2_yanchao(self):
        current_time_hour, current_time_min = self.__get_current_time()
        result = {
            "current_time": f"{current_time_hour}:{current_time_min}",
            "next_stop": None,
            "all_info": None
        }
        found = False
        for item in self.HePing2YanChao.copy():
            for stops in item['stops']:
                stop_time = stops['time']
                if stops['note'] == '下車':
                    continue
                if int(stop_time.split(':')[0]) == current_time_hour and int(
                        stop_time.split(':')[1]) >= current_time_min or int(
                    stop_time.split(':')[0]) > current_time_hour:
                    result['next_stop'] = stops.copy()
                    result['next_stop']['location'] = self.locations[stops['name']]
                    result['all_info'] = item
                    found = True
                    break
            if found:
                break
        return result

    def get_all_school_bus_schedule_heping_2_yanchao(self):
        return self.HePing2YanChao

    def get_location_info(self, location=None):
        if location is None:
            raise Exception("location is None")
        return self.locations[location]


if __name__ == '__main__':
    bus = SchoolBus()
    print(bus.get_next_school_bus_schedule_yanchao_2_heping())
