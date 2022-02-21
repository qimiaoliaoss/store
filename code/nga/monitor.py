# -*- coding: utf-8 -*-
# @Time : 2022/1/25 12:32
# @Author : Losir
# @FileName: monitor_all.py
# @Software: PyCharm

import sys
import requests, json
from requests import exceptions
import time
import os
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
basedir = os.path.abspath(os.path.dirname(__file__))
father_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
config_path = basedir + '/config.ini'
print(config_path)
config.read(config_path, encoding="utf-8")
header = config['account']['header']
cookie = config['account']['ck']
key = config['target']['key_words']
tid = json.loads(config['target']['tid'])
flag = 0
# path = "page.txt"
platform_sys = platform.system()
if platform_sys == 'Windows':
    path = "page.txt"
    time_path = "time.txt"
    status_path = "../status.txt"
elif platform_sys == 'Linux':
    path = basedir + "/page.txt"
    time_path = basedir + "/time.txt"
    status_path = father_path + "/status.txt"
# 帖子ID
tid = "30607982"
# 楼主ID
uid = "6818580"
urllib3.disable_warnings()

print(basedir, father_path, path, time_path, status_path)
header = json.loads(header)
cookie = json.loads(cookie)
key = json.loads(key)
print(tid)
print(key)
url1 = "https://bbs.nga.cn/read.php?tid=" + str(tid) + "&page=code"
# url1 = "https://bbs.nga.cn/thread.php?fid=570&order_by=postdatedesc"
# res = requests.get(url1, headers=header, verify=False, timeout=10, cookies=cookie).content.decode('GBK',errors='ignore')
now = time.strftime("%Y-%m-%d %H:%M:%S")

class Spider:
    def load(self):
        pass

    def get_page(self):
        pass

    def get_speak(self):
        pass

# if __name__ == "__main__":

print('-------运行时间：{}'.format(now) + '-------')
# try:
#     with open(path, "r+") as f:
#         compared = f.readlines()
#         print(compared)
#     tmp_url = "https://bbs.nga.cn/"
#     url1 = "https://bbs.nga.cn/thread.php?fid=706&order_by=postdatedesc"
#     # print(url1)
#     res = requests.get(url1, headers=head, verify=False, timeout=10, cookies=cook).content.decode('GBK',
#                                                                                                   errors='ignore')
#     # print(res)
#     if "访客不能直接访问" in str(res):
#         raise Exception("Cookie失效请更新")
#     html = etree.HTML(res)
#     # match = tmp_url + test[0]
#     m1 = re.compile(r"id='(.+?)' title='用户ID " + uid + "'")
#     # 61078637
#     target = m1.findall(res)
#     # print(target)
#     if target:
#         print("目标：" + str(target))
#         replaced = []
#         for each in target:
#             replaced.append(each.replace("a1", "t1"))
#         print("替换：" + str(replaced))
#         new = ''
#         for each in replaced:
#             print(each)
#             tmp_title = str(html.xpath('//*[@id="' + each + '"]/text()')[0])
#             # all(tmp_title not in s for s in compared)
#             if all(tmp_title not in s for s in compared):
#                 flag = 1
#                 title = "标题：" + tmp_title
#                 change_time = each.replace("tt1", "pt1")
#                 print(change_time)
#                 # date = "发帖时间：" + str(html.xpath('//*[@id="' + each.replace("ta1", "pt1") + '"]'))
#                 url = "https://bbs.nga.cn/" + html.xpath('//*[@id="' + each + '"]/@href')[0]
#                 print(url)
#                 print(title)
#                 new = new + title + "\n" + url + "\n"
#                 with open(path, "a+") as f:
#                     f.write(tmp_title + '\n')
#         print(new)
#     # time.sleep(3)
# except Exception as e:
#     if "HTTPSConnectionPool" not in str(e):
#         print(e)
#         flag = 1
#         new = str(e)
# # except exceptions.Timeout as e:
# #     print(str(e))
# now = time.strftime("%Y-%m-%d %H:%M:%S")
print('-------结束时间：{}'.format(now) + '-------')