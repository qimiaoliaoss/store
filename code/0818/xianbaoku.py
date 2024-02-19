# -*- coding: utf-8 -*-
# @Time : 2023/10/9 17:25
# @Author : Losir
# @FileName: xianbaoku.py
# @Software: PyCharm
import requests
import sys

enable_notification = 1   #0不发送通知   1发送通知


# 只有在需要发送通知时才尝试导入notify模块
if enable_notification == 1:
    try:
        from notify import send
    except ModuleNotFoundError:
        print("警告：未找到notify.py模块。它不是一个依赖项，请勿错误安装。程序将退出。")
        sys.exit(1)

# 设置请求头
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "timezone=8",
    "Host": "new.xianbao.fun",
    "If-Modified-Since": "Mon, 09 Oct 2023 09:29:37 GMT",
    "If-None-Match": "\"6523c801-16f4\"",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

# 设置GET请求的URL
url = "http://new.xianbao.fun/plus/json/push_16.json"

# 发送GET请求
response = requests.get(url, headers=headers)

# 检查响应是否成功
if response.status_code == 200:
    print("请求成功")
    response_data = response.json()
    # print(response_data)

    check_list = ['流量', '话费', '大水', '建行', '建设银行', '工行', '工商银行', '立减金', '零元', '麦当劳', '金拱门', '麦辣', '板烧', '脆汁鸡', '礼盒']

    with open('xbk.txt', 'r', encoding='utf-8') as f:
        recorded_titles = set(line.strip() for line in f)

    new_titles = []

    for item in response_data:
        if any(keyword in item["title"] or keyword in item["content"] for keyword in check_list):
            title = item["title"]
            if title not in recorded_titles:
                new_titles.append(title)
                new = "{}\n{}\n{}".format(item["title"], item["content"], "http://new.xianbao.fun" + item["url"])
                title = "[线报]{}".format(item["title"])
                content = "{}\n{}".format(item["content"], "https://re.breathefreely.icu" + item["url"])
                print(new)
                if enable_notification == 1:
                    send(title, content)

    if new_titles:
        with open('xbk.txt', 'a', encoding='utf-8') as f:
            for title in new_titles:
                f.write(title + '\n')
else:
    print("Failed to fetch data. Status code: {}".format(response.status_code))

