# -*- coding: utf-8 -*-
# @Time : 2024/5/9 14:48
# @Author : Losir
# @FileName: check_ip.py
# @Software: PyCharm
# 验证代理IP有效性
import requests

url = "http://httpbin.org/ip"
proxies = {"http": "http://192.168.31.180:5858", "https": "http://192.168.31.180:5858"}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
}
try:
    resp = requests.get(url, headers=headers, proxies=proxies)
    print(resp.text)
except Exception as e:
    print(f"请求失败，代理IP无效！{e}")
