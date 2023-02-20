# -*- coding: utf-8 -*-
# @Time : 2023/2/20 15:47
# @Author : Losir
# @FileName: main.py
# @Software: PyCharm

from wxpusher import WxPusher

app_token = 'AT_y9LC5MoroUv3BzdxlS4NZJYwAd1TifVl'  # 本处改成自己的应用 APP_TOKEN
uid_myself = ['UID_UjdtZpFQDc89AOpdzgYDzbHTgVsS', 'UID_BuzmpfjD7ikdCbRQiJg3I2qDi6ZU']  # 本处改成自己的 UID
topic_id = '8898'


def wxpusher_send_by_sdk(msg, uid):
    """利用 wxpusher 的 python SDK ，实现微信信息的发送"""
    result = WxPusher.send_message(msg,
                                   uids=[uid],
                                   # topic_ids=topic_id,
                                   token=app_token,
                                   summary=msg)
    return result


def main(msg):
    for each in uid_myself:
        # result1 = wxpusher_send_by_webapi(msg)
        result2 = wxpusher_send_by_sdk(msg, each)
        # print(result1)
        print(result2)


if __name__ == '__main__':
    main('gv该保号了\n互助号码：(470) 354-4029，(413) 758-9548，(507) 403-8587')
