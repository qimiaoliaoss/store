# -*- coding: utf-8 -*-
# @Time : 2023/5/26 14:31
# @Author : Losir
# @FileName: main.py
# @Software: PyCharm
import requests
import json
from datetime import datetime, timezone, timedelta


def main():
    timezone_1 = timezone(timedelta(hours=8))
    url = "https://weibo.com/ajax/statuses/mymblog?uid=7769778635&page=1&feature=0"

    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Cookie': 'XSRF-TOKEN=iviBIqPXJuuK_iOdqT8R2vnw; SUB=_2AkMTLNUnf8NxqwFRmfkXzW3kaYxzww7EieKlcCT8JRMxHRl-yT9vqnZStRB6OKz7yCac7cbolPuQCcRCOzonkD4TnqAF; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5EXnGCOUZiBSbrCw8ZUYX3; WBPSESS=HOKMwFaOhMG7Cl30d6Y-8XIBLMI452kWIDg2ckiQniXNxwCnVZF61EfEdhSiWWjQoKl4he5G0MuW0aEV-D05O52gLQTbZCEyX1X92EVhQU-rpvz7uy18TnJLdj7behY7',
        'Sec-Ch-Ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    response = requests.get(url=url, headers=header)
    result = json.loads(response.content.decode('utf-8'))
    with open("./time.txt", "r") as f:
        new_time = f.readlines()[0]
    # new_time = '2023-05-26 10:31:10+08:00'
    print(new_time)
    new_time = datetime.fromisoformat(new_time)
    for item in result['data']['list']:
        # 将给定时间字符串转换为 datetime 对象
        datetime_obj = datetime.strptime(item['created_at'], "%a %b %d %H:%M:%S %z %Y")
        # 获取当前时间，并设置时区信息为给定时间的时区信息
        current_time = datetime.now(timezone.utc).astimezone(datetime_obj.tzinfo)
        # current_time = "2023-05-26 13:19:27+08:00"
        # current_time = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S%z")
        # print("当前时间：{}".format(current_time))
        # 比较给定时间是否早于当前时间
        if new_time < datetime_obj:
            new_time = datetime_obj
            print("新发言，时间已更新".format(datetime_obj))
            print(item['text'])
            with open("./time.txt", "w+") as f:
                f.write(str(new_time))
        else:
            print("{}发帖时间晚于或等于当前时间".format(datetime_obj))


if __name__ == "__main__":
    main()
