# -*- coding: utf-8 -*-
# @Time : 2023/7/13 22:20
# @Author : DanYang
# @File : data_processing.py
# @Software : PyCharm
import json

import pandas as pd

with open("GUI/results.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)

with open("image_results.txt", "r") as file:
    image_data = file.readlines()

new_json_data = []
estimations = ["非常差", "差", "一般", "好", "非常好"]
for j_data, i_data in zip(json_data, image_data):
    data = {
        **j_data["factor"],
        **j_data["goal"]
    }
    for pos, i in enumerate(list(i_data.strip())):
        data[f"factor{pos}"] = int(i)
    new_json_data.append(data)

df = pd.DataFrame(columns=new_json_data[0].keys())
for data in new_json_data:
    df = df.append(data, ignore_index=True)
df.to_excel("results.xlsx", header=["视频类型", "视频封面", "视频标题", "视频简介", "视频时长（秒）", "视频发布时间", "播放量", "弹幕量", "评论量",
                                    "收藏量", "投币量", "分享量", "点赞量", "视觉吸引力", "信息传达", "情感引发", "与UP主风格一致", "点击率预测"])

