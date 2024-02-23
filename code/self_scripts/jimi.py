# -*- coding: utf-8 -*-
# @Time : 2024/2/23 14:58
# @Author : Losir
# @FileName: jimi.py
# @Software: PyCharm
import datetime
import requests
import json
import os
import sys
import io
from notify import send
enable_notification = 1   #0不发送通知   1发送通知
# 只有在需要发送通知时才尝试导入notify模块
if enable_notification == 1:
    try:
        from notify import send
    except ModuleNotFoundError:
        print("警告：未找到notify.py模块。它不是一个依赖项，请勿错误安装。程序将退出。")
        sys.exit(1)
# 去除warning
requests.packages.urllib3.disable_warnings()

class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for file in self.files:
            file.write(obj)
            file.flush()

    def flush(self):
        for file in self.files:
            file.flush()


def sign():
    try:
        url_signin = 'https://mobile-api.xgimi.com/app/v4/integral/signin'
        url_getPage = 'https://mobile-api.xgimi.com/app/v4/view/getPage'
        # 请求头部参数
        headers = {
            "openId": "92c0c042c7abce45ad04f0b89ff6c3c1",
            "accessToken": accessToken,
            "timestamp": "1693917654891",
            "sign": "e075727aa75cd6b7f3c60567bb312372",
            "Host": "mobile-api.xgimi.com",
            "User-Agent": "okhttp/4.9.1",
            "Content-Length": "31"
        }
        headers2 = {
            "openId": "92c0c042c7abce45ad04f0b89ff6c3c1",
            "accessToken": accessToken,
            "timestamp": "1693917654891",
            "sign": "e075727aa75cd6b7f3c60567bb312372",
            "Host": "mobile-api.xgimi.com",
            "User-Agent": "okhttp/4.9.1",
            "Content-Length": "31"
        }
        # 请求体参数
        data_signin = {'configNo': '2021061111211168'}
        data_getPage = {"currentPage": 1, "pageSize": 12, "viewId": "10003"}

        # 发送POST请求
        response_signin = requests.post(url_signin, headers=headers, data=json.dumps(data_signin))
        response_getPage = requests.post(url_getPage, headers=headers2, data=json.dumps(data_getPage))

        # 输出响应内容
        res = json.loads(response_signin.content.decode())
        res2 = json.loads(response_getPage.content.decode())
        print('签到响应{}'.format(res))
        # print('个人信息响应{}'.format(res2))
        score = json.loads(res2['data']['sections'][0]['extend'])['score']
        recentSeriesTime = json.loads(res2['data']['sections'][1]['extend'])['recentSeriesTime']
        new = '极米签到通知\n\n当前积分:{}\n连续签到天数:{}\n'.format(score, recentSeriesTime)

        if res['data']['status']:
            if res['data']['status'] == 3:
                print('签到成功')
                new += '签到成功'
            elif res['data']['status'] == 2:
                print('{}今日已签到'.format(now))
                new += '{}今日已签到'.format(now)
            else:
                print('未知错误')
                new += '未知错误\n' + res['message']
            print(new)
        else:
            print('未知错误')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # 获取当前时间
    now = datetime.datetime.now()
    # 输出时间戳
    print(now)
    accessToken = os.getenv('jimi_ac')
    print(accessToken)
    # 开启数据流
    captured_output = io.StringIO()
    original_stdout = sys.stdout
    sys.stdout = Tee(sys.stdout, captured_output)

    sign()

    # 关闭数据流
    sys.stdout = original_stdout
    output_content = captured_output.getvalue()
    captured_output.close()

    if enable_notification == 1:
        send("极米签到 通知", output_content)
