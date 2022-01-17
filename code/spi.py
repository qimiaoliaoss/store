# -*- coding: utf-8 -*-
# @Time : 2021/12/25 13:50
# @Author : Losir
# @FileName: spi.py
# @Software: PyCharm

import sys
import requests, json
import time
import random
from lxml import etree
from bs4 import *
import urllib3
import platform
import json
import configparser
requests.packages.urllib3.disable_warnings()
before_url = "https://bbs.nga.cn/"
config = configparser.ConfigParser()
config.read('config.ini')
header = config['account']['header']
cookie = config['account']['ck']
tid = config['account']['tid']
uid = config['account']['uid']
header = json.loads(header)
cookie = json.loads(cookie)
print(type(cookie))
print('tid:' + tid + '\nuid:' + uid)
url1 = "https://bbs.nga.cn/read.php?tid=" + tid + "&page=code"
res = requests.get(url1, headers=header, verify=False, timeout=10, cookies=cookie).content.decode('GBK',
                                                                                                  errors='ignore')
# print(res)
