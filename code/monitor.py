# -*- coding: utf-8 -*-
# @Time : 2022/1/25 12:32
# @Author : Losir
# @FileName: monitor.py
# @Software: PyCharm

import sys
import requests, json
from requests import exceptions
import time
import random
from lxml import etree
from bs4 import *
import urllib3
import platform
platform_sys = platform.system()
import json
import configparser
requests.packages.urllib3.disable_warnings()
before_url = "https://bbs.nga.cn/"
config = configparser.ConfigParser()
config.read('config.ini', encoding="utf-8")
header = config['account']['header']
cookie = config['account']['ck']
key = config['target']['key_words']
header = json.loads(header)
cookie = json.loads(cookie)
print(key)
# url1 = "https://bbs.nga.cn/read.php?tid=" + tid + "&page=code"
url1 = "https://bbs.nga.cn/thread.php?fid=570&order_by=postdatedesc"
# res = requests.get(url1, headers=header, verify=False, timeout=10, cookies=cookie).content.decode('GBK',errors='ignore')
now = time.strftime("%Y-%m-%d %H:%M:%S")
print('-------运行时间：{}'.format(now) + '-------')
try:
    with open(path, "r+") as f:
        compared = f.readlines()
        print(compared)
    tmp_url = "https://bbs.nga.cn/"
    url1 = "https://bbs.nga.cn/thread.php?fid=706&order_by=postdatedesc"
    # print(url1)
    res = requests.get(url1, headers=head, verify=False, timeout=10, cookies=cook).content.decode('GBK',
                                                                                                  errors='ignore')
    # print(res)
    if "访客不能直接访问" in str(res):
        raise Exception("Cookie失效请更新")
    html = etree.HTML(res)
    # match = tmp_url + test[0]
    m1 = re.compile(r"id='(.+?)' title='用户ID " + uid + "'")
    # 61078637
    target = m1.findall(res)
    # print(target)
    if target:
        print("目标：" + str(target))
        replaced = []
        for each in target:
            replaced.append(each.replace("a1", "t1"))
        print("替换：" + str(replaced))
        new = ''
        for each in replaced:
            print(each)
            tmp_title = str(html.xpath('//*[@id="' + each + '"]/text()')[0])
            # all(tmp_title not in s for s in compared)
            if all(tmp_title not in s for s in compared):
                flag = 1
                title = "标题：" + tmp_title
                change_time = each.replace("tt1", "pt1")
                print(change_time)
                # date = "发帖时间：" + str(html.xpath('//*[@id="' + each.replace("ta1", "pt1") + '"]'))
                url = "https://bbs.nga.cn/" + html.xpath('//*[@id="' + each + '"]/@href')[0]
                print(url)
                print(title)
                new = new + title + "\n" + url + "\n"
                with open(path, "a+") as f:
                    f.write(tmp_title + '\n')
        print(new)
    # time.sleep(3)
except Exception as e:
    if "HTTPSConnectionPool" not in str(e):
        print(e)
        flag = 1
        new = str(e)
# except exceptions.Timeout as e:
#     print(str(e))
now = time.strftime("%Y-%m-%d %H:%M:%S")
print('-------结束时间：{}'.format(now) + '-------')