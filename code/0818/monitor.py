# -*- coding: utf-8 -*-
# @Time : 2022/6/15 12:13
# @Author : Losir
# @FileName: monitor.py
# @Software: PyCharm

import requests
import json
from lxml import etree
import platform
import time, os
import configparser

requests.packages.urllib3.disable_warnings()


def get_proxy():
    return requests.get("https://" + proxy + "/get/").json()


def delete_proxy(proxy):
    requests.get("https://" + proxy + "/delete/?proxy={}".format(proxy))


def get_HTML(url1):
    retry_count = 3
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            html = requests.get(url1, headers=header, cookies=cookie, proxies={"http": "http://{}".format(proxy)},
                                verify=False,
                                timeout=3)
            # 使用代理访问
            print("查询成功")
            return html
        except Exception as e:
            result = 'Except：' + str(e) + "Line：" + str(e.__traceback__.tb_lineno)
            print(result)
            retry_count -= 1
    # 删除代理池中代理
    err = "error"
    delete_proxy(proxy)
    return err


def get_target(url1):
    try:
        with open(path, 'r+', encoding='utf-8') as f:
            old = f.readlines()
            for i in range(len(old)):
                old[i] = old[i].replace('\n', '')
            print("有%d条旧记录" % len(old))
            res = get_HTML(url1)
            # print(res.content.decode('GBK'))
            if res != 'error' and res.status_code == 200:
                print("读取页面内容")
                html = res.content.decode('utf-8')
                et_html = etree.HTML(html)
                title = et_html.xpath('//*[@id="redtag"]/a')
                # print(title)
                for i in range(len(title)):
                    tl = title[i].attrib.get('title')
                    dz = 'http://www.0818tuan.com' + title[i].attrib.get('href')
                    # if ('京东' in tl or '京东' in tl or '建行' in tl) and tl not in old:
                    if (any(list_ele in tl for list_ele in list)) and tl not in old:
                        print('%s 地址：%s' % (tl, dz))
                        f.write(tl + '\n')
                        # notify(tl, dz)
                        new = tl + '\n' + dz
                        access_token, expires_in = get_access_token(corp_id, corp_secret)
                        wechat_push_text(agent_id=agent_id, access_token=access_token, message=new)
            else:
                print('路上过于拥堵')
    except Exception as e:
        result = 'Except：' + str(e) + "Line：" + str(e.__traceback__.tb_lineno)
        print(result)


def notify(tl, new):
    api = "https://sctapi.ftqq.com/" + serverchen_key + ".send"
    title = '有线报'
    content = '%s 地址：%s' % (tl, new)
    data = {
        "text": title,
        "desp": content
    }
    req = requests.post(api, verify=False, timeout=10, data=data).content.decode('utf-8')
    print(req)


def get_access_token(corp_id, corp_secret):
    resp = requests.get(f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={corp_secret}')
    js = json.loads(resp.text)
    print(js)
    if js["errcode"] == 0:
        access_token = js["access_token"]
        expires_in = js["expires_in"]
        return access_token, expires_in


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
    print(js)
    if js["errcode"] == 0:
        return js


if __name__ == '__main__':
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    print('-------运行时间：{}'.format(now) + '-------')
    config = configparser.ConfigParser()
    basedir = os.path.abspath(os.path.dirname(__file__))
    father_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
    config_path = basedir + r'\config.ini'
    print('config_path：' + config_path)
    config.read(config_path, encoding="utf-8")
    header = json.loads(config['account']['header'])
    cookie = json.loads(config['account']['ck'])
    proxy = json.loads(config['DEFAULT']['proxy'])
    serverchen_key = json.loads(config['serverchen']['key'])
    corp_id = json.loads(config['wechat']['corp_id'])
    corp_secret = json.loads(config['wechat']['corp_secret'])
    agent_id = json.loads(config['wechat']['agent_id'])
    # print(cookie)
    list = ['大水', '建行', '建设银行']
    platform_sys = platform.system()
    if platform_sys == 'Windows':
        path = "xb.txt"
    elif platform_sys == 'Linux':
        path = "/root/0818/xb.txt"
    url = 'http://www.0818tuan.com/list-1-0.html'
    get_target(url)
