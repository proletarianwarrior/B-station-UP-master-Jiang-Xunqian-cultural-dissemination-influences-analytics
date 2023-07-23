# -*- coding: utf-8 -*-
# @Time : 2023/7/11 14:58
# @Author : DanYang
# @File : Spider.py
# @Software : PyCharm
import json
import hashlib
import time
import datetime

import yaml
import requests


class BiliSpider:
    def __init__(self):
        with open("config.yaml", "r") as file:
            self.yaml_data = yaml.safe_load(file)
        self.headers = self.yaml_data["headers"]
        self.save_path = self.yaml_data["save_path"]

    def web_rid(self, param):
        n = "653657f524a547ac981ded72ea172057" + "6e4909c702f846728e64f6007736a338"
        c = ''.join([n[i] for i in
                     [46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49, 33, 9, 42, 19, 29, 28,
                      14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54,
                      21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52]][:32])
        s = int(time.time())
        param["wts"] = "1684737775"
        param = "&".join([f"{i[0]}={i[1]}" for i in sorted(param.items(), key=lambda x: x[0])])
        return hashlib.md5((param + c).encode(encoding='utf-8')).hexdigest(), s

    def get_main_page(self, pn):
        main_page_url = self.yaml_data["urls"]["main_page"]
        params = self.yaml_data["params"].copy()
        params["pn"] = pn
        params["w_rid"] = params["w_rid"][pn - 1]
        params["wts"] = params["wts"][pn - 1]
        response = requests.get(url=main_page_url, params=params, headers=self.headers)

        return response.json()

    def get_detail_page(self, aid):
        detail_url = self.yaml_data["urls"]["detail_page"].format(aid=aid)
        response = requests.get(url=detail_url, headers=self.headers)

        return response.json()

    def parse_main_page(self, json_data):
        video_list = json_data["data"]["list"]["vlist"]
        aid_list = [video["aid"] for video in video_list]
        length_list = [video["length"] for video in video_list]
        time_list = [video["created"] for video in video_list]
        date_list = [datetime.datetime.fromtimestamp(t) for t in time_list]

        return aid_list, length_list, date_list

    def parse_detail_page(self, json_data):
        data = json_data["data"]
        tname = data["tname"]
        pic = data["pic"]
        title = data["title"]
        desc = data["desc"]
        stat = data["stat"]
        owner_name = data["owner"]["name"]

        if owner_name == "江寻千":
            detail_data = {
                "factor": {
                    "tname": tname,
                    "pic": pic,
                    "title": title,
                    "desc": desc
                },
                "goal": {
                    "view": stat["view"],
                    "danmaku": stat["danmaku"],
                    "reply": stat["reply"],
                    "favorite": stat["favorite"],
                    "coin": stat["coin"],
                    "share": stat["share"],
                    "like": stat["like"]
                }
            }
        else:
            return None
        return detail_data

    def merge_data(self, length_datas, date_datas, detail_datas):
        def change_to_second(time_string):
            split_string = time_string.split(":")
            minute = int(split_string[0])
            second = int(split_string[1])
            return minute * 60 + second
        length_datas = [change_to_second(length) for length in length_datas]

        result_data = []
        for length, date, detail in zip(length_datas, date_datas, detail_datas):
            if not detail:
                continue
            detail["factor"]["length"] = length
            detail["factor"]["date"] = date.strftime("%Y-%m-%d %H:%M:%S")
            result_data.append(detail)

        return result_data

    def main_crawl(self):
        main_result_data = []
        for page in range(1, 7):
            main_data = self.get_main_page(pn=page)
            aid_data, length_data, date_data = self.parse_main_page(main_data)
            detail_data = [self.get_detail_page(aid) for aid in aid_data]
            detail_data = [self.parse_detail_page(detail) for detail in detail_data]
            result_data = self.merge_data(length_data, date_data, detail_data)
            main_result_data.extend(result_data)

        with open(self.save_path, "w", encoding="utf-8") as file:
            json.dump(main_result_data, file, indent=3, ensure_ascii=False)


if __name__ == '__main__':
    spider = BiliSpider()
    spider.main_crawl()
