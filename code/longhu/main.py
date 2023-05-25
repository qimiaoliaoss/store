# -*- coding: utf-8 -*-
# @Time : 2023/5/11 16:29
# @Author : Losir
# @FileName: main.py
# @Software: PyCharm
import time
import execjs
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import requests
import urllib3
from lxml import etree
import re
import redis
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


# r = redis.Redis(host='localhost', port=6379, db=0)
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
        # r.set('youzi_dict', json.dumps(youzi_dict))
    except Exception as e:
        print('错误信息：' + str(e) + "，错误行数：" + str(e.__traceback__.tb_lineno))


def main():
    try:
        # value = r.get('youzi_dict')
        # youzi_list = json.loads(value.decode())
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
            if '退' not in name[i] and '转债' not in name[i] and code[i][:2] not in ["82", "83", "87", "88"] and code[i][
                                                                                                              :3] not in [
                "900"]:
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
                if tmp not in ['融资融券', '转融券标的', '富时罗素概念股', '标普道琼斯A股', '沪股通', '富时罗素概念', '深股通']:
                    print(tmp)
                    my_list.append(tmp)
            print("------------------------")
            time.sleep(10)
        print(my_list)
        text = ' '.join(my_list)
        # ls = jieba.lcut(text)  # 生成分词列表
        # text = ' '.join(ls)  # 连接成字符串
        stop_words = {'你', '我', '他', '啊', '的', '了', '2022', '明天', '今天', '怎么', '记录', '讨论', '雪球', '没有', '是不是', '吐槽', '融资',
                      '融券', '富时', '罗素', '与'}
        word_freq = dict(Counter(my_list))
        print(word_freq)
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


def test():
    my_list = ['骨传导', '智能穿戴', '音乐产业', '智能音箱', '无线耳机', '深股通', '融资融券', '转融券标的', '迪士尼', '口罩', '消费电子概念', '电子竞技', '电子商务',
               '广告营销', '文化传媒', '网络游戏', '手机游戏', 'ST板块', '网约车', '跨境电商', '电子商务', '网络直播', '抖音概念', '拼多多概念', '新零售', '数字经济',
               '阿里巴巴概念', '虚拟数字人', '社区团购', '虚拟现实', '跨境电商', '宠物经济', '粤港澳大湾区', '高送转预期', '电子商务', '网络直播', '新零售', '虚拟数字人',
               '三胎概念', '正极材料', '锂电池', '地方国企改革', '转融券标的', '新股与次新股', '融资融券', '新零售', '老字号', '国企改革', '重庆国企改革', '三胎概念',
               '医疗器械概念', '超级品牌', '网络直播', '深股通', '电子商务', '芯片概念', '注册制次新股', '转融券标的', '新股与次新股', '融资融券', '中芯国际概念', '深股通',
               '节能环保', '金改', '小额贷款', '大数据', '华为概念', '独角兽概念', '区块链', '口罩', '腾讯概念', '快手概念', '抖音概念', '参股银行', '共同富裕示范区',
               'ST板块', '物业管理', '汽车制造概念', '转融券标的', '机器人概念', '工业机器人', '航空航天', '比亚迪概念', '人民币贬值受益', '智能制造', '工业4.0', '高端装备',
               '无人机', '机器视觉', '融资融券', '新能源汽车', '新股与次新股', '注册制次新股', '壳资源', '光伏概念', '融资融券', '转融券标的', '沪股通', '电子竞技',
               '东北亚经贸中心', '文化传媒', '网络游戏', 'IP概念', '影视娱乐', '手机游戏', '互联网金融', '富时罗素概念股', '快手概念', '元宇宙', '大数据', '东数西算（算力）',
               '数字经济', '抖音概念', '融资融券', '转融券标的', '虚拟现实', 'web3.0', '跨境电商', '数据确权', '在线教育', '乡村振兴', '信创', 'ChatGPT概念',
               '百度概念', '深股通', '人工智能', 'AIGC概念', '数据要素', '虚拟数字人', '余额宝', '电子商务', '电子信息', '百度金融', '金融信息服务', '互联网保险',
               '腾讯概念', '融资融券', '人工智能', '沪股通', '转融券标的', '金融科技', '国产软件', '独角兽概念', '互联网金融', '区块链', '富时罗素概念', '富时罗素概念股',
               '智慧城市', '标普道琼斯A股', '数字货币', '数字经济', '信创', '锌二氧化锰', '污水处理', '小金属概念', '节能环保', '宁德时代概念', '电解锰', '磷酸铁锂',
               '金属锰', '锂电池', '金属镍', '比亚迪概念', '钠离子电池', '融资融券', '转融券标的', '地方国企改革', '湖南国企改革', '国企改革', '深股通', '吡啶', '农村电商',
               '乡村振兴', '标普道琼斯A股', 'ST板块', '富时罗素概念股', '草甘膦', '草地贪夜蛾防治', '智能电网', '能源互联网', '充电桩', '虚拟电厂', '电力物联网',
               '新股与次新股', '网络直播', '三胎概念', '抗病毒面料', '抖音概念', '新零售', '粤港澳大湾区', '广东自贸区', '电子商务', 'WIN升级', '全息手机', '触摸屏',
               '壳资源', '柔性屏', '消费电子概念', 'ST板块', '3D打印', '激光器', '光纤', '横琴新区', '激光', '5G', '芯片概念', '无人驾驶', '量子科技', '股权转让',
               '融资融券', '转融券标的', '地方国企改革', '国企改革', '深股通', '共封装光学（CPO）', '送转填权', '广东国企改革', '珠海国企改革', '王者荣耀', '电子信息',
               '成渝特区', '5G', '智能家居', '光纤', '大数据', '物联网', '智慧城市', '边缘计算', '超清视频', '华为概念', '光纤光缆', '云计算', 'VPN', '云游戏',
               '云办公', '在线教育', '数据中心', '标普道琼斯A股', '数字中国', '富时罗素概念股', 'ST板块', '腾讯概念', '东数西算（算力）', '数字经济', '百度概念', '京东概念',
               '转融券标的', '染料', '新股与次新股', '融资融券', '转融券标的', '比亚迪概念', '特斯拉', '新股与次新股', '融资融券', '专精特新', '海洋经济', '参股保险',
               '水产品', '预制菜', '人民币贬值受益', '中字头股票', '地方国企改革', '央企国企改革', '国企改革', '区块链', '激光', '燃料电池', '网络安全', '信创',
               '医疗器械概念', '智能制造', '安防', '光伏概念', '数字经济', '数据安全', 'NFT概念', '云计算', 'ST板块', '工业4.0', '集成电路概念', '存储芯片',
               '机器人概念', '京津冀一体化', '富时罗素概念', '蚂蚁金服概念', '参股万达商业', '标普道琼斯A股', '旅游', '环球主题公园', '商超百货', '参股银行', '富时罗素概念股',
               '新零售', 'ST板块', '一元股', '融资融券', '转融券标的', '新股与次新股', '机器视觉', '芯片概念', '科创次新股', '机器人概念', '传感器', '虚拟现实', '人工智能',
               '人脸识别', '蚂蚁金服概念', '阿里巴巴概念', '雷达', 'AI芯片', '在线教育', '芯片设计', '服务机器人', 'MLOps概念', '3D打印', '云计算', '边缘计算',
               '数字孪生', '电子商务', '广告营销', '文化传媒', '新零售', '网红经济', 'C2M概念', '工业机器人', '机器人概念', '抖音概念', '污水处理', 'PPP概念',
               '新股与次新股', '核准制次新股', '一带一路', '两江新区', '融资融券', '深股通', '转融券标的', '富时罗素概念', '富时罗素概念股', '物业管理', '标普道琼斯A股',
               'MSCI概念', '托育服务', '三胎概念', '富士康概念', '安防', '国产替代', '专精特新', '消费电子概念', '外贸受益概念', '机器视觉', '人工智能', '虚拟现实',
               '电力改革', '碳交易', '节能电机', 'IGBT', '工业机器人', '机器人概念', '燃料电池', '物联网', '工业互联网', '稀土永磁', '云计算', '数据中心', '集成电路概念',
               '透明工厂', '储能', '光伏建筑一体化', '光伏概念', '换电概念', '新能源汽车', '充电桩', '轨道交通', '氢能源', '融资融券', '转融券标的', '工业母机',
               '粤港澳大湾区', '深股通', '一季报预增', 'PPP概念', '一带一路', '智能物流', '首都副中心', '融资融券', '深股通', '转融券标的', '京津冀一体化', '特色小镇',
               '雄安新区', '旅游', '富时罗素概念', '富时罗素概念股', '标普道琼斯A股', 'MSCI概念', '一元股', '中医药', 'NMN概念', '仿制药一致性评价', '医美概念',
               '幽门螺杆菌概念', '新冠治疗', '流感', '蒙脱石散', '肝炎概念', '一季报预增', '三星', '数据存储', '元器件', '内存', '知识产权保护', '芯片概念', '融资融券',
               '转融券标的', '人民币贬值受益', '粤港澳大湾区', '地方国企改革', '国企改革', '存储芯片', '物联网', '转融券标的', '云办公', '新股与次新股', '融资融券', '华为概念',
               '注册制次新股', '腾讯概念', '数字经济', '数据安全', '军工', '节能环保', '节能电机', '核电', '一带一路', '标普道琼斯A股', '核污染防治', '地方国企改革',
               '山东国企改革', '国企改革', '送转填权', '摘帽', '转融券标的', '专精特新', '注册制次新股', '融资融券', '减速器', '新股与次新股', '机器人概念', '航空航天',
               '工业机器人', '军工', '工业4.0', '特斯拉', '机器人概念', '新基建', '创业板重组松绑', '无人机', '比亚迪概念', '融资融券', '转融券标的', '深股通',
               '转融券标的', '专精特新', '比亚迪概念', '新股与次新股', '融资融券', '新能源汽车', '机器人概念', '类稀土', '稀缺资源', '锌二氧化锰', '小金属概念', '锂电池',
               '金属锰', '正极材料', '融资融券', '转融券标的', '地方国企改革', '山东国企改革', '国企改革', '沪股通', 'OLED', '柔性屏', '光刻胶', '转融券标的', '融资融券',
               '专精特新', '智能表', '物联网', '5G', '边缘计算', '华为概念', '镍氢电池', '智慧城市', '芯片概念', '云计算', '移动支付', '智能物流', '智慧停车',
               '数据中心', '充电桩', '粤港澳大湾区', '新能源汽车', '军工', '机器人概念', '高端装备', '智能制造', '物联网', '智能物流', '融资融券', '人工智能', '工业互联网',
               '建筑节能', '转融券标的', '比亚迪概念', '高送转预期', '黄金租赁', '3D打印', '小金属概念', '黄金概念', '抖音小店', '杭州亚运会', '冬奥纪念品', '北京国企改革',
               '地方国企改革', '国企改革', '参股银行', '冬奥会', 'ST板块', '宽带中国', '物联网', '智能家居', '5G', '工业互联网', '新基建', '边缘计算', '华为概念',
               '融资融券', '转融券标的', '人民币贬值受益', 'F5G概念', 'WiFi 6', '共封装光学（CPO）', '东北亚经贸中心', '振兴东北', '大连自贸区', '地方国企改革',
               '辽宁国企改革', '国企改革', '摘帽', '棉', '供销社', '乡村振兴', '农机', '转融券标的', '传感器', '注册制次新股', '融资融券', '新股与次新股', '专精特新',
               '储能', '智能电网', '虚拟电厂', '国产替代', '新能源', '高送转预期', '物联网', '云计算', '人工智能', '大数据', '工业4.0', '边缘计算', '数据中心',
               '传感器', '机器人概念', '电力改革', '节能环保', '光伏概念', '分布式发电', '煤炭概念', '浙江国企改革', '地方国企改革', '国企改革', '核准制次新股', '新股与次新股',
               '新能源汽车', '机器人概念', '智能家居', '专精特新', '蔚来汽车概念', '长三角一体化', '比亚迪概念', '毫米波雷达', '中朝贸易区', '校车', '汽车制造概念', '融资租赁',
               '新能源整车', '新能源汽车', '燃料电池', '军工', 'ST板块']
    stop_words = {'你', '我', '他', '啊', '的', '了', '2022', '明天', '今天', '怎么', '记录', '讨论', '雪球', '没有', '是不是', '吐槽', '融资',
                  '融券', '富时', '罗素', '与', '融资融券', '概念', '转', '转融券标的'}
    word_freq = dict(Counter(my_list))
    print(word_freq)
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


if __name__ == "__main__":
    main()
    # test()
