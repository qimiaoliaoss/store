# -*- coding: utf-8 -*-
# @Time : 2023/5/11 16:29
# @Author : Losir
# @FileName: main.py
# @Software: PyCharm

import requests
import urllib3
from lxml import etree
import re
import redis
import json

urllib3.disable_warnings()
r = redis.Redis(host='localhost', port=6379, db=0)


def youzi():
    try:
        youzi_dict = {}
        for i in range(1, 62):
            url = 'https://www.aijingu.com/youzi/' + str(i) + '.html'
            info_heards = {
                'Host': 'data.10jqka.com.cn',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
                'Referer': 'https://www.google.com/',
                'Cookie': 'refreshStat=off; v=Azqun_-eCunCB4YF0EPkfuaPi2tZ67-GMG4yYEQy5GqY1dTVLHsO1QD_gnsX',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
            }
            response = requests.get(url=url, headers=info_heards, verify=False)
            # print(response.status_code)
            html = etree.HTML(response.content.decode('utf-8', errors='ignore'))
            text = html.xpath('/html/body/div[3]/div[1]/p[1]/text()')
            if text:
                match = re.search(r"(.*)简介", text[0])
                if match:
                    name = match.group(1).strip()  # 获取匹配结果并删除空格
                    # print(name)
                    text_2 = list(set(html.xpath('/html/body/div[3]/div[3]/div/table/tbody/tr/td[9]/a/text()')))
                    youzi_dict[name] = text_2
                    describe = html.xpath('/html/body/div[3]/div[1]/p[2]/text()')[0].strip()
                    # print(text_2)
                    # print('{}、{}：{}\n营业部：{}'.format(i, name, describe, ','.join(text_2)))
                else:
                    print("页面内无匹配游资名称")
            else:
                print("{}无页面".format(i))
        print(youzi_dict)
        r.set('youzi_dict', json.dumps(youzi_dict))
    except Exception as e:
        print('错误信息：' + str(e) + "，错误行数：" + str(e.__traceback__.tb_lineno))


def main():
    try:
        value = r.get('youzi_dict')
        youzi_list = json.loads(value.decode())
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
        price = html.xpath('//*[@id="ggmx"]/div[2]/div[3]/div[1]/div/div/table/tbody/tr/td[7]/text()')
        # three = html.xpath('//*[@id="ggmx"]/div[2]/div[3]/div[1]/div/div/table/tbody/tr/td[1]/label/text()')
        if len(code) == len(name):
            for i in range(len(code)):
                print("------------------------")
                try:
                    three = html.xpath(
                        '//*[@id="ggmx"]/div[2]/div[3]/div[1]/div/div/table/tbody/tr[' + str(i+1) + ']/td['
                                                                                                    '1]/label/text('
                                                                                                    ')')[0]
                except Exception as e:
                    # print(e)
                    three = ''
                # print(three)
                if three == '3日':
                    print('|{}|{}：{}，净买入额：{}'.format(three, code[i], name[i], price[i]))
                elif three == '':
                    print('{}：{}，净买入额：{}'.format(code[i], name[i], price[i]))
                buy = html.xpath('//*[@id="ggmx"]/div[2]/div[3]/div[2]/div[' + str(
                    i + 1) + ']/div[2]/table[1]/tbody/tr/td[1]/a/@title')
                sell = html.xpath('//*[@id="ggmx"]/div[2]/div[3]/div[2]/div[' + str(
                    i + 1) + ']/div[2]/table[2]/tbody/tr/td[1]/a/@title')
                print('买入席位：')
                for k in range(len(buy)):
                    for key, value in youzi_list.items():
                        if buy[k] in value and key != 'T王':
                            print('  {}：{}'.format(key, buy[k]))
                print('卖出席位：')
                for k in range(len(sell)):
                    for key, value in youzi_list.items():
                        if sell[k] in value and key != 'T王':
                            print('  {}：{}'.format(key, sell[k]))
                print("------------------------")
    except Exception as e:
        print('Except：' + str(e) + "，Line：" + str(e.__traceback__.tb_lineno))


if __name__ == "__main__":
    main()
