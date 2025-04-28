# -*- coding: utf-8 -*-
# @Time : 2025/2/17 11:29
# @Author : Losir
# @FileName: main.py
# @Software: PyCharm
import os
import requests

print(requests.get("https://akshare.akfamily.xyz/").content.decode('utf-8'))