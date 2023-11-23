# -*- coding: utf-8 -*-
# @Time : 2023/11/23 11:49
# @Author : Losir
# @FileName: checkin.py
# @Software:
import re
from datetime import datetime, time
from chinese_calendar import is_holiday, is_workday
from notify import serverJ

def check_in():
    # 定义正则表达式模式
    pattern = re.compile(rf"{current_date}上班(\d{{4}})")

    # 进行匹配
    match = pattern.search(input_string)

    if match:
        work_time = match.group(1)
        title = f"上班成功"
        content = f"匹配成功，上班时间为: {work_time}"
        print(content)
        serverJ(title, content)
    else:
        print("匹配失败")


def check_out():
    # 定义正则表达式模式
    pattern = re.compile(rf"{current_date}下班(\d{{4}})")

    # 进行匹配
    match = pattern.search(input_string)

    if match:
        work_time = match.group(1)
        title = f"下班成功"
        content = f"匹配成功，下班时间为: {work_time}"
        print(content)
        serverJ(title, content)
    else:
        print("匹配失败")


if __name__ == "__main__":
    # 从文件中读取字符串
    with open("day.txt", "r", encoding="utf-8") as file:
        input_string = file.read().strip()
    # print(input_string)
    # 获取当前日期和时间
    current_datetime = datetime.now()
    current_date = current_datetime.date()
    current_time = current_datetime.time()
    nine_am = time(9, 0, 0)
    six_pm = time(18, 0, 0)

    print("当前日期:{}，当前时间:{}".format(current_date, current_time))
    if is_workday(current_date):
        print("当前为工作日")
        if nine_am < current_time < six_pm:
            print("判断上班打卡")
            check_in()
        elif current_time >= six_pm:
            print("判断下班打卡")
            check_out()
