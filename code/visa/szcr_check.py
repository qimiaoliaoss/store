# -*- coding: utf-8 -*-
# @Time : 2024/5/15 9:50
# @Author : Losir
# @FileName: szcr_check.py
# @Software: PyCharm
import requests
import json
from sendNotify import send
# 去除warning
requests.packages.urllib3.disable_warnings()


def sign():
    try:
        url = 'https://vtravel.link2shops.com/vfuliApi/api/client/localife/goods/recommendNewList'
        # 请求头部参数
        headers = {
            'Host': 'vtravel.link2shops.com',
            'Connection': 'keep-alive',
            'Content-Length': '133',
            'xweb_xhr': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/8323',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://servicewechat.com/wxdf6dfe1316e2bc72/44/page-frame.html',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh'
        }
        # 请求体参数
        data = {
            "pageTag": "szcr",
            "platformType": "小程序",
            "terminalType": "other",
            "zxId": "",
        }

        # 发送POST请求
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # 输出响应内容
        res = json.loads(response.content.decode())
        data = res['data']
        # print(data)
        filtered_data = [item for item in data if item['zxName'] == '影音娱乐']

        if not filtered_data:
            print('没有找到符合条件的数据')
        else:
            for item in filtered_data:
                list_data = item['list']
                filtered_list = [sub_item for sub_item in list_data if sub_item['name'] == '哔哩哔哩大会员(月卡)']

                if not filtered_list:
                    print('没有找到符合条件的子数据')
                else:
                    for sub_item in filtered_list:
                        name = sub_item['name']
                        stock = sub_item['stock']
                        send_content = '{}库存：{}'.format(name, stock)
                        print(send_content)
                        if stock == 1:
                            print('有库存，开始推送')
                            new = 'VISA卡上新了'
                            send(new, send_content)
                        else:
                            print('无库存')
    except Exception as e:
        print('未知错误{}'.format(e))


def main():
    sign()


if __name__ == "__main__":
    main()
