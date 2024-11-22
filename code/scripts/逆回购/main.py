# -*- coding: utf-8 -*-
# @Time : 2024/11/22 11:03
# @Author : Losir
# @FileName: main.py
# @Software: PyCharm
import json
import re
import requests


def get_reverse_repo_price():
    url = "https://hq.stock.sohu.com/cn/810/cn_131810-1.html"
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "gidinf=x099980109ee18695dc141c49000b73929f3229326ca; SUV=1714124625360cecjvl; BIZ_MyLBS=cn_131810%2CR-001%7C; t=1732244222653; reqtype=pc; _dfp=j0vBwXIQ/upvLCe3FFA7WbT2OomWce0MtPvLQnS20MU=",
        "referer": "https://static.k.sohu.com/",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "script",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 确保请求成功

    # 使用正则提取 `fortune_hq` 函数中的 JSON 数据
    match = re.search(r"fortune_hq\((\{.*?\})\);", response.text)
    if not match:
        raise ValueError("无法提取 JSON 数据")

    # 清理提取到的 JSON 数据
    json_str = match.group(1)

    pattern = r'"price_A1":\["([a-zA-Z0-9_]+)","([^"]+)","([^"]+)","([^"]+)","([^"]+)","([^"]+)"\]'

    matches = re.search(pattern, json_str)

    if matches:
        stock_code = matches.group(1)  # 股票代码
        stock_name = matches.group(2)  # 股票名称
        price = matches.group(3)  # 价格
        change = matches.group(4)  # 涨跌
        percent_change = matches.group(5)  # 涨幅
        volume = matches.group(6)  # 成交量

        print(f"股票代码: {stock_code}")
        print(f"股票名称: {stock_name}")
        print(f"价格: {price}")
        print(f"涨跌: {change}")
        print(f"涨幅: {percent_change}")
        print(f"成交量: {volume}")
    else:
        print("未找到匹配数据")

    # 修复 JSON 格式问题
    # 1. 替换所有的单引号为双引号
    json_str = json_str.replace("'", "\"")

    # 2. 对于嵌套数组，可能会有不合法的部分，需要将其转化为合法格式
    json_str = re.sub(r'\"(\[\s*[\d,.\"\s]*\])\"', r'\1', json_str)  # 清理嵌套的数组字符串

    try:
        # 解析 JSON 数据
        data = json.loads(json_str)

        # 提取价格信息
        price_info = data.get("price_A1")
        if not price_info:
            raise ValueError("无法找到价格信息")

        price = price_info[2]  # 当前价格
        change = price_info[4]  # 涨跌幅

        return price, change
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 解析错误: {e}")


# 测试函数
if __name__ == "__main__":
    try:
        price, change = get_reverse_repo_price()
        print(f"当前价格: {price}, 涨跌幅: {change}")
    except Exception as e:
        print(f"发生错误: {e}")


