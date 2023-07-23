# -*- coding: utf-8 -*-
# @Time : 2023/7/12 13:01
# @Author : DanYang
# @File : hand_coded.py
# @Software : PyCharm
import json
from io import BytesIO
import tkinter as tk

from PIL import ImageTk, Image
import requests

root = tk.Tk()

label_0 = tk.Label(root,
                   text="以下图片与标题分别选自B站UP主江千寻的视频封面与视频标题，请阅读以下五种指标含义，回答你对该视频各个指标的评价。",
                   fg="red", font=("Arial", 12))
label_1 = tk.Label(root,
                   text="1. 视觉吸引力（Visual Appeal）：评估封面在视觉上的吸引力和美观程度。考虑颜色搭配、构图、元素排列等因素。")
label_2 = tk.Label(root,
                   text="2. 信息传达（Information Conveyance）：评估封面是否能够清晰地传达视频的主题、内容或情感。考虑文字、图像、符号等元素的表达是否准确和明确。")
label_3 = tk.Label(root,
                   text="3. 情感引发（Emotional Engagement）：评估封面是否能够引发情感共鸣或兴趣。考虑封面所传达的情绪、情感色彩、与目标受众的契合程度等因素。")
label_4 = tk.Label(root,
                   text="4. 与UP主风格一致性（Consistency with UP主's Style）：评估封面是否与UP主的风格、品牌形象相一致。考虑UP主过去的封面设计风格、色彩偏好、排版等因素。")
label_5 = tk.Label(root,
                   text="5. 点击率预测（Clickability）：评估封面是否具有吸引用户点击的潜力。考虑封面中的关键元素、吸引人眼球的特点、与目标受众的契合度等因素。")

label_0.grid(row=0, column=0, sticky="w")
label_1.grid(row=1, column=0, sticky="w")
label_2.grid(row=2, column=0, sticky="w")
label_3.grid(row=3, column=0, sticky="w")
label_4.grid(row=4, column=0, sticky="w")
label_5.grid(row=5, column=0, sticky="w")

with open("results.json", "r", encoding="utf-8") as file:
    data = json.load(file)
print(len(data))

label_image = tk.Label(root)
label_title = tk.Label(root, font=("Arial", 20), fg="red")
label_desc = tk.Label(root, font=("Arial", 20), fg="blue")
label_image.grid(row=6, column=0)
label_title.grid(row=7, column=0)
label_desc.grid(row=8, column=0)

image_num = 0
tk_image = None


def get_image(image_num):
    global tk_image
    url = data[image_num]["factor"]["pic"]
    title = data[image_num]["factor"]["title"]
    desc = data[image_num]["factor"]["desc"] if data[image_num]["factor"]["desc"] else "无"
    response = requests.get(url)
    image_data = response.content
    image = Image.open(BytesIO(image_data))
    image = image.resize((int(2050 / 3), int(1150 / 3)))
    tk_image = ImageTk.PhotoImage(image)

    return tk_image, title, desc


image, title, desc = get_image(image_num)
label_image.config(image=image)
label_title.config(text=f"标题：{title}")
label_desc.config(text=f"简介：{desc}")

var = tk.IntVar()
var.set(0)
label_names = ["1. 视觉吸引力", "2. 信息传达", "3. 情感引发", "4. 与UP主风格一致性", "5. 点击率预测"]
kind_num = 0
int_list = []
label_kind = tk.Label(root, text=label_names[kind_num], font=("Arial", 15), fg="red")
label_kind.grid(row=9, column=0, sticky="s")


def turn_next_question():
    global kind_num, int_list
    kind_num += 1
    int_list.append(var.get())
    if kind_num == 5:
        with open("results.txt", "r") as file:
            lines = file.readlines()
        string = "".join([str(i) for i in int_list])
        if len(lines) > image_num:
            lines[image_num] = string + "\n"
        else:
            lines.append(string + "\n")
        print(lines)
        with open("results.txt", "w") as file:
            file.write("".join(lines))
        int_list = []
    if kind_num < 5:
        label_kind.config(text=label_names[kind_num])
    var.set(0)


radio_button_1 = tk.Radiobutton(root, text="非常差", variable=var, value=1, command=turn_next_question)
radio_button_2 = tk.Radiobutton(root, text="差", variable=var, value=2, command=turn_next_question)
radio_button_3 = tk.Radiobutton(root, text="一般", variable=var, value=3, command=turn_next_question)
radio_button_4 = tk.Radiobutton(root, text="好", variable=var, value=4, command=turn_next_question)
radio_button_5 = tk.Radiobutton(root, text="非常好", variable=var, value=5, command=turn_next_question)

radio_button_1.grid(row=10, column=0, sticky="s")
radio_button_2.grid(row=11, column=0, sticky="s")
radio_button_3.grid(row=12, column=0, sticky="s")
radio_button_4.grid(row=13, column=0, sticky="s")
radio_button_5.grid(row=14, column=0, sticky="s")


entry = tk.Entry(root)
def page_change():
    global image_num
    image_num = int(entry.get())
    image, title, desc = get_image(image_num - 1)
    label_image.config(image=image)
    label_title.config(text=f"标题：{title}")
    label_desc.config(text=f"简介：{desc}")


button_page = tk.Button(root, text="确定", command=page_change)
button_page.grid(row=16, column=1)
entry.grid(row=15, column=1)


def next_click():
    global image_num, kind_num
    if kind_num < 5:
        return
    kind_num = 0
    label_kind.config(text=label_names[0])
    image_num += 1
    image, title, desc = get_image(image_num)
    label_image.config(image=image)
    label_title.config(text=f"标题：{title}")
    label_desc.config(text=f"简介：{desc}")


def before_click():
    global image_num, kind_num
    if kind_num < 5:
        return
    kind_num = 0
    label_kind.config(text=label_names[0])
    image_num -= 1
    image, title, desc = get_image(image_num)
    label_image.config(image=image)
    label_title.config(text=f"标题：{title}")
    label_desc.config(text=f"简介：{desc}")


button_before = tk.Button(root, text="上一页", command=before_click)
button_next = tk.Button(root, text="下一页", command=next_click)

button_before.grid(row=15, column=0, sticky="s")
button_next.grid(row=16, column=0, sticky="s")


root.mainloop()
