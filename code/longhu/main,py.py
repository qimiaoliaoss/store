# -*- coding: utf-8 -*-
# @Time : 2023/5/11 16:29
# @Author : Losir
# @FileName: main,py.py
# @Software: PyCharm

import requests
import urllib3
from lxml import etree
from prettytable import PrettyTable
import re

urllib3.disable_warnings()


def youzi():
    try:
        url = 'https://www.aijingu.com/youzi/index.html'
        info_heards = {
            'Host': 'data.10jqka.com.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'Referer': 'https://www.google.com/',
            'Cookie': 'refreshStat=off; v=Azqun_-eCunCB4YF0EPkfuaPi2tZ67-GMG4yYEQy5GqY1dTVLHsO1QD_gnsX',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }
        response = requests.get(url=url, headers=info_heards, verify=False).content.decode('utf-8', errors='ignore')
        html = etree.HTML(response)
        text = html.xpath('/html/body/div[3]/div[1]/div/div/div/ul/li[1]/a/text()')
        pattern = r'(\d+)-(\d+)/(\d+)'
        if len(text) == 1:
            match = re.search(pattern, text[0])
            if match:
                total_num = match.group(3)
                print(total_num)
                if int(total_num) < 50:
                    page = 1
                else:
                    page = (int(total_num) - 50) // 50 + 2
                for each in range(page):
                    url = 'https://www.aijingu.com/youzi/index.html?page=' + str(each + 1)
                    response = requests.get(url=url, headers=info_heards, verify=False).content.decode('utf-8', errors='ignore')
                    html = etree.HTML(response)
        else:
            print("游资列表匹配错误")
            exit(0)
    except Exception as e:
        print('Except：' + str(e) + "，Line：" + str(e.__traceback__.tb_lineno))


def main():
    try:
        tables = []
        url = 'https://data.10jqka.com.cn/market/longhu/'
        info_heards = {
            'Host': 'data.10jqka.com.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'Referer': 'https://www.google.com/',
            'Cookie': 'refreshStat=off; v=Azqun_-eCunCB4YF0EPkfuaPi2tZ67-GMG4yYEQy5GqY1dTVLHsO1QD_gnsX',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }
        response = requests.get(url=url, headers=info_heards, verify=False).content.decode('GBK', errors='ignore')
        # result = response.json()
        html = etree.HTML(response)
        code = html.xpath('//*[@id="ggmx"]/div[2]/div[3]/div[1]/div/div/table/tbody/tr/td[2]/text()')
        name = html.xpath('//*[@id="ggmx"]/div[2]/div[3]/div[1]/div/div/table/tbody/tr/td[3]/a/text()')
        for l in range(len(code)):
            tables.append(PrettyTable())
        if len(code) == len(name):
            for i in range(len(code)):
                buy = html.xpath('//*[@id="ggmx"]/div[2]/div[3]/div[2]/div[' + str(i + 1) + ']/div[2]/table[1]/tbody/tr/td[1]/a/@title')
                sell = html.xpath('//*[@id="ggmx"]/div[2]/div[3]/div[2]/div[' + str(i + 1) + ']/div[2]/table[2]/tbody/tr/td[1]/a/@title')
                tables[i].field_names = ["买入金额最大的前5名营业部", "卖出金额最大的前5名营业部"]
                print('{}：{}\n买入前五：'.format(code[i], name[i]))
                for k in range(len(buy)):
                    tables[i].add_row([buy[k], sell[k]])
                print(tables[i])
    except Exception as e:
        print('Except：' + str(e) + "，Line：" + str(e.__traceback__.tb_lineno))


if __name__ == "__main__":
    youzi()
