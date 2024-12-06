# -*- coding: utf-8 -*-
# @Time : 2023/10/9 16:00
# @Author : Losir
# @FileName: check.py
# @Software: PyCharm
import requests
import json
from notify import serverJ

# 设置请求头
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Length": "52",
    "Content-Type": "application/json;charset=UTF-8",
    "Host": "vtravel.link2shops.com",
    "Origin": "https://vtravel.link2shops.com",
    "Referer": "https://vtravel.link2shops.com/ccbyiyuan/?uuid=kgDWcIhfScYKRG16H3xVrcvo6tRALdU8in1DBE0XIRc=",
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1",
    "token": "[object Object]"
}

# 设置POST请求的URL
url = "https://vtravel.link2shops.com/vfuliApi/api/client/ypJyActivity/goodsList"

# 设置POST请求的JSON数据
data = {
    "activityTag": "ccbyyg",
    "catagoryId": ""
}

# 发送POST请求
response = requests.post(url, headers=headers, json=data)

# 解析JSON响应
response_data = json.loads(response.text)

# 查找"20元京东E卡"的库存状态
for goods in response_data["data"]["goodsList"]:
    if goods["name"] == "20元京东E卡":
        if goods["stockStatus"] == "2":
            print("20元京东E卡已售罄")
        else:
            print("20元京东E卡还有库存")
            title, content = "20元京东E卡还有库存"
            serverJ(title, content)
        break