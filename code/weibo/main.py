# -*- coding: utf-8 -*-
# @Time : 2023/5/26 14:31
# @Author : Losir
# @FileName: main.py
# @Software: PyCharm
import requests
import json
from datetime import datetime
import configparser
import os
import time
from requests_toolbelt import MultipartEncoder
import platform


def get_access_token(corp_id, corp_secret):
    resp = requests.get(f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={corp_secret}')
    js = json.loads(resp.text)
    # print(js)
    if js["errcode"] == 0:
        access_token = js["access_token"]
        expires_in = js["expires_in"]
        return access_token, expires_in


def wechat_push_img(agent_id, access_token, media_id):
    data = {
        "touser": "@all",
        "msgtype": "image",
        "agentid": agent_id,
        "image": {
            "media_id": media_id
        },
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    # print(data)
    resp = requests.post(f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}&debug=1',
                         json=data)
    js = json.loads(resp.text)
    # print(js)
    if js["errcode"] == 0:
        print('图片发送成功')
        return js
    else:
        print(js)


def wechat_push_text(agent_id, access_token, message):
    data = {
        "touser": "@all",
        "msgtype": 'text',
        "agentid": agent_id,
        "text": {
            "content": message
        },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    resp = requests.post(f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}', json=data)
    js = json.loads(resp.text)
    # print(js)
    if js["errcode"] == 0:
        return js


def upload_img(filename, access_token):
    post_file_url = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={}&type=image'.format(access_token)
    m = MultipartEncoder(
        fields={filename: ('file', open(current_dir + filename, 'rb'), 'text/plain')},
    )
    r = requests.post(url=post_file_url, data=m, headers={'Content-Type': m.content_type})
    # print(r.text)
    r = json.loads(r.text)
    # print(r['media_id'])
    return r['media_id']


def main(corp_id, corp_secret, agent_id, time_file_path):
    try:
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
        with open(time_file_path, "r") as f:
            new_time = f.readlines()[0]
        # new_time = '2023-05-26 10:31:10+08:00'
        print("已记录的发言时间为{}".format(new_time))
        new_time = datetime.fromisoformat(new_time)
        tmp = new_time
        access_token, expires_in = get_access_token(corp_id, corp_secret)
        for item in result['data']['list']:
            # 将给定时间字符串转换为 datetime 对象
            datetime_obj = datetime.strptime(item['created_at'], "%a %b %d %H:%M:%S %z %Y")
            # 比较给定时间是否早于当前时间
            if new_time < datetime_obj:
                if item['pic_ids']:
                    print('有图片')
                    pic_url = []
                    media = []
                    for each in item['pic_ids']:
                        pic_url.append('https://wx2.sinaimg.cn/mw690/' + each + '.jpg')
                    # print(pic_url)
                    for each in pic_url:
                        header_2 = {
                            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Accept-Language': 'zh-CN,zh;q=0.9',
                            'Cache-Control': 'no-cache',
                            'Pragma': 'no-cache',
                            'Referer': 'https://weibo.com/',
                            'Sec-Ch-Ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
                            'Sec-Ch-Ua-Mobile': '?0',
                            'Sec-Ch-Ua-Platform': '"Windows"',
                            'Sec-Fetch-Dest': 'image',
                            'Sec-Fetch-Mode': 'no-cors',
                            'Sec-Fetch-Site': 'cross-site',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
                        }
                        response = requests.get(url=each, headers=header_2)
                        if response.status_code == 200:
                            # 从URL中获取文件名
                            filename = each.split("/")[-1]
                            # 保存图片到本地
                            with open(filename, "wb") as file:
                                file.write(response.content)
                            print(f"图片保存成功：{filename}")
                            media_tmp = upload_img(filename, access_token)
                            wechat_push_img(agent_id, access_token, media_tmp)
                        else:
                            print("请求失败")
                if tmp < datetime_obj:
                    tmp = datetime_obj
                print("{}新发言，时间已更新".format(datetime_obj))
                print(item['text'])
                new = "微博发言：\n" + item['text']
                wechat_push_text(agent_id=agent_id, access_token=access_token, message=new)
            else:
                print("{}非新发言".format(datetime_obj))
        new_time = tmp
        with open(time_file_path, "w+") as f:
            f.write(str(new_time))
    except Exception as e:
        result = 'Except：' + str(e) + "，Line：" + str(e.__traceback__.tb_lineno)
        print(result)
        new = "访问出错\n" + result
        wechat_push_text(agent_id=agent_id, access_token=access_token, message=new)


if __name__ == "__main__":
    op = time.time()
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    print('-------运行时间：{}'.format(now) + '-------')
    config = configparser.ConfigParser()
    current_os = platform.system()
    if current_os == 'Windows':
        current_dir = os.getcwd() + '\\'
    elif current_os == 'Linux':
        current_dir = os.getcwd() + '/'
    basedir = os.path.abspath(os.path.dirname(__file__))
    father_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
    config_path = basedir + r'/config.ini'
    time_file_path = basedir + r'/time.txt'
    print('config_path：' + config_path)
    config.read(config_path, encoding="utf-8")
    corp_id = json.loads(config['wechat']['corp_id'])
    corp_secret = json.loads(config['wechat']['corp_secret'])
    agent_id = json.loads(config['wechat']['agent_id'])
    main(corp_id, corp_secret, agent_id, time_file_path)
    elapsed = (time.time() - op)
    print('-------用时：{}'.format(elapsed) + '-------')
