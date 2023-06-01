# -*- coding: utf-8 -*-
# @Time : 2023/5/11 16:29
# @Author : Losir
# @FileName: main.py
# @Software: PyCharm
import time
import execjs
from wordcloud import WordCloud
import requests
import urllib3
from lxml import etree
import re
import json
import datetime
from collections import Counter

urllib3.disable_warnings()
session = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}
session.headers = headers
today = datetime.datetime.now()
str_today = today.strftime('%Y-%m-%d')
start_day = datetime.datetime.now() + datetime.timedelta(days=-31)
str_start_day = start_day.strftime('%Y-%m-%d')


def get_proxy():
    return requests.get("https://proxy.ionssource.cn/get/").json()


def delete_proxy(proxy):
    requests.get("https://proxy.ionssource.cn/delete/?proxy={}".format(proxy))


def get_server_time():
    url = 'http://www.iwencai.com/unifiedwap/home/index'
    resp = session.get(url)
    resp_text = resp.text
    tree = etree.HTML(resp_text)
    js_url = "http:" + tree.xpath("//script[1]/@src")[0]
    resp.close()
    js_resp = session.get(js_url)
    js_text = js_resp.text
    obj = re.compile(r'var TOKEN_SERVER_TIME=(?P<time>.*?);!function')
    server_time = obj.search(js_text).group('time')
    return server_time


def get_hexin_v(time):
    f = open("kou.js", "r", encoding='utf-8')
    js_content = f.read()
    js_content = 'var TOKEN_SERVER_TIME=' + str(time) + ";\n" + js_content
    js = execjs.compile(js_content)
    v = js.call("rt.updata")
    return v


def get_answer(question, secondary_intent):
    url = 'http://www.iwencai.com/customized/chart/get-robot-data'

    data = {
        'add_info': "{\"urp\":{\"scene\":1,\"company\":1,\"business\":1},\"contentType\":\"json\",\"searchInfo\":true}",
        'block_list': "",
        'log_info': "{\"input_type\":\"typewrite\"}",
        'page': 1,
        'perpage': 50,
        'query_area': "",
        'question': question,
        'rsh': "Ths_iwencai_Xuangu_y1wgpofrs18ie6hdpf0dvhkzn2myx8yq",
        'secondary_intent': secondary_intent,
        'source': "Ths_iwencai_Xuangu",
        'version': "2.0"
    }

    session.headers['hexin-v'] = get_hexin_v(get_server_time())
    session.headers['Content-Type'] = 'application/json'
    resp = session.post(url, data=json.dumps(data))
    result = resp.json()
    resp.close()
    return result


def wencai():
    data = get_answer('今日涨停的股票；非ST；所属概念；连板天数；最终涨停时间', 'stock')
    result = data['data']['answer'][0]['txt'][0]['content']['components'][0]['data']['datas']
    # print(result)
    big_list = []
    for i in result:
        # print(i)
        if '所属概念' in i:
            big_list += i['所属概念'].split(';')
    counter = dict(Counter(big_list))
    to_del = ['融资融券', '转融券标的', '华为概念', '富时罗素概念股', '标普道琼斯A股', '沪股通', '富时罗素概念', '深股通', '国企改革', '地方国企改革']
    for deling in to_del:
        try:
            del counter[deling]
        except:
            pass
    # print(counter)
    stop_words = {'你', '我', '他', '啊', '的', '了', '2022', '明天', '今天', '怎么', '记录', '讨论', '雪球', '没有', '是不是', '吐槽', '融资',
                  '融券', '富时', '罗素', '与'}
    word_cloud = WordCloud(font_path=r"C:\Windows\Fonts\SimHei.ttf",
                           width=1000,
                           height=700,
                           background_color="white",
                           stopwords=stop_words)
    word_cloud.generate_from_frequencies(counter)
    # word_cloud.generate(text)
    # print(text_cut)
    file_name = '%s.png' % time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    word_cloud.to_file(file_name)


def main():
    try:
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
        tmp_code = []
        for i in range(len(code)):
            if '退' not in name[i] and '转债' not in name[i] and code[i][:2] not in ["82", "83", "87", "88"] and code[i][:3] not in ["900"]:
                tmp_code.append(code[i])
        my_code = list(set(tmp_code))
        my_list = []
        print(my_code)
        lenth = len(my_code)
        v = get_hexin_v(get_server_time())
        print(v)
        for i in range(lenth):
            count = 0
            status = 0
            print("------------{}/{}------------".format(i + 1, lenth))
            print(my_code[i])
            while status != 200:
                if 0 < count < 11:
                    print("重试第{}次".format(count))
                    print(response_2.content)
                elif count == 11:
                    print("超出重试上限")
                    exit(0)
                url2 = 'https://www.iwencai.com/diag/block-detail?pid=8153&codes=' + my_code[i] + '&info={"view":{' \
                                                                                                  '"nolazy":1}} '
                info_heards = {
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Connection': 'keep-alive',
                    'Cookie': 'other_uid=Ths_iwencai_Xuangu_ibrcdbuosv0p2pxztix0j8506d3ltatm; '
                              'ta_random_userid=kbyr8bxw65; cid=a3b7fd4992fcd47cbe076952eebffde01684921421; '
                              'wencai_pc_version=0; cid=a3b7fd4992fcd47cbe076952eebffde01684921421; '
                              'ComputerID=a3b7fd4992fcd47cbe076952eebffde01684921421; WafStatus=0; '
                              'PHPSESSID=07884dccb6e6fdd0070172a60d0d7e49; '
                              'iwencaisearchquery=%E9%BE%99%E8%99%8E%E6%A6%9C; '
                              'v=' + v,
                    'Hexin-V': v,
                    'Host': 'www.iwencai.com',
                    'Referer': 'http://www.iwencai.com/stockpick/search?rsh=3&typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w={}'.format(
                        my_code[i]),
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest'
                }
                response_2 = requests.get(url=url2, headers=info_heards, verify=False)
                print(response_2.status_code)
                status = response_2.status_code
                count += 1
                time.sleep(3)
            result_2 = json.loads(response_2.content)
            # print(result_2['data']['data']['tableTempl'])
            html_2 = etree.HTML(json.dumps(result_2['data']['data']['tableTempl']))
            bland = html_2.xpath('//table/tbody/tr/td[4]/div/span/a/text()')
            for each in bland:
                tmp = each.encode('utf-8').decode('unicode_escape')
                if tmp not in ['融资融券', '转融券标的', '富时罗素概念股', '标普道琼斯A股', '沪股通', '富时罗素概念', '深股通', '国企改革', '地方国企改革', '华为概念']:
                    print(tmp)
                    my_list.append(tmp)
            print("------------------------")
            time.sleep(5)
        print(my_list)
        text = ' '.join(my_list)
        # ls = jieba.lcut(text)  # 生成分词列表
        # text = ' '.join(ls)  # 连接成字符串
        stop_words = {'你', '我', '他', '啊', '的', '了', '2022', '明天', '今天', '怎么', '记录', '讨论', '雪球', '没有', '是不是', '吐槽', '融资',
                      '融券', '富时', '罗素', '与'}
        word_freq = dict(Counter(my_list))
        # print(word_freq)
        word_cloud = WordCloud(font_path=r"C:\Windows\Fonts\SimHei.ttf",
                               width=1000,
                               height=700,
                               background_color="white",
                               stopwords=stop_words)
        word_cloud.generate_from_frequencies(word_freq)
        # word_cloud.generate(text)
        # print(text_cut)
        file_name = '%s.png' % time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        word_cloud.to_file(file_name)

    except Exception as e:
        print('Except：' + str(e) + "，Line：" + str(e.__traceback__.tb_lineno))


if __name__ == "__main__":
    # main()
    wencai()
