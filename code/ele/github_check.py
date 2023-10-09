# -*- coding: utf-8 -*-
# @Time : 2023/9/27 11:34
# @Author : Losir
# @FileName: github_check.py
# @Software: PyCharm

import requests

url = 'https://github.com/pingxingsheng/elm'
res = requests.get(url, timeout=3)
if r'This is not the web page you are looking for' in res.content.decode():
    print(True)