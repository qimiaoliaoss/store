# -*- coding: utf-8 -*-
# @Time : 2024/4/15 15:57
# @Author : Losir
# @FileName: main.py.py
# @Software: PyCharm
import configparser
import json
import os
import platform
import re
import threading
import time
import requests
from lxml import etree
from notify import send

# 获取操作环境
platform_sys = platform.system()
# 去除warning
requests.packages.urllib3.disable_warnings()


def get_proxy():
    return requests.get("https://{}/get/".format(proxyurl)).json()


def delete_proxy(proxy):
    requests.get("https://{}/delete/?proxy={}".format(proxyurl, proxy))

def get_HTML(url1):
    retry_count = 5
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            html = requests.get(url1, headers=header, proxies={"http": "http://{}".format(proxy)}, verify=False,
                                timeout=10, cookies=cookie)
            # 使用代理访问
            print("查询成功")
            return html
        except Exception:
            retry_count -= 1
    # 删除代理池中代理
    err = "error"
    delete_proxy(proxy)
    return err


def get_page(tar, thread_num):
    try:
        flag = 0
        print('---------------------\n线程%d正在访问%s' % (thread_num, config[tar]["name"]))
        key = config[tar]["name"]
        url1 = "https://bbs.nga.cn/thread.php?fid=570&order_by=postdatedesc"
        # print(url1)
        retry_count = 5
        proxy = get_proxy().get("proxy")
        while retry_count > 0:
            try:
                res = requests.get(url1, headers=header, proxies={"http": "http://{}".format(proxy)}, verify=False
                                   , timeout=10, cookies=cookie)
                break
            except Exception:
                retry_count -= 1
                print("代理重试次数剩余%d" % retry_count)
        else:
            delete_proxy(proxy)
            raise Exception('代理失效')
        res_html = res.content.decode('GBK', errors='ignore')
        # print(res_html)
        if res.status_code == 200:
            # if config['DEFAULT']['status'] != '200':
            if config[tar]['status'] != '200':
                print("网络已恢复，置入200")
                config.set(tar, 'status', '200')
                config.write(open(config_path, "r+", encoding="utf-8"))
            html = etree.HTML(res_html)
            # match = tmp_url + test[0]
            m1 = re.compile(r"id='(.+?)' class='topic'>[^.]*?" + key + ".*?")
            # target = m1.findall(res_html)
            # print(html.xpath('//*[@id="pagebbtm"]/script/text()'))
            try:
                target = m1.findall(res_html)
            except Exception:
                end = '1'
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
                    if all(tmp_title not in s for s in compared):
                        flag = 1
                        title = "标题：" + tmp_title
                        change_time = each.replace("tt1", "pt1")
                        print(change_time)
                        url = "https://bbs.nga.cn/" + html.xpath('//*[@id="' + each + '"]/@href')[0]
                        print(url)
                        print(title)
                        new = new + title + "\n" + url + "\n"
                        with open(path, "a+") as f:
                            f.write(tmp_title + '\n')
                print(new)
        else:
            print("进入%s帖子错误，等待恢复" % config[tar]["name"])
            if config[tar]['status'] == '200':
                config.set(tar, 'status', str(res.status_code))
                config.write(open(config_path, "r+", encoding="utf-8"))
                new = "进入%s帖子错误，等待恢复" % config[tar]["name"]
                flag = 1
            # config[tar]["status"] = str(res.status_code)
    except Exception as e:
        result = 'Except：' + str(e) + "Line：" + str(e.__traceback__.tb_lineno)
        print(result)
        flag = 1
        new = '泥潭羊毛报错:' + str(result)

    if flag == 1:
        # notify(new, tar)
        send(new, tar)


def test(tar, num):
    # print(config[tar])
    time.sleep(10)
    print("线程%d,%s开始睡觉" % (num, config[tar]['name']))


if __name__ == "__main__":
    op = time.time()
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    # if platform_sys == 'Windows':
    #     path = "已推送.txt"
    # elif platform_sys == 'Linux':
    #     path = "/root/nga/已推送.txt"
    path = os.path.abspath(os.path.dirname(__file__)) + '/已推送.txt'
    print('-------运行时间：{}'.format(now) + '-------')
    proxyurl = os.getenv('proxyurl')
    with open(path, "r+") as f:
        compared = f.readlines()
        # print(compared)
    # config.ini模块初始化，目录路径初始化
    config = configparser.ConfigParser()
    basedir = os.path.abspath(os.path.dirname(__file__))
    father_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
    config_path = basedir + '/config.ini'
    print('config_path：' + config_path)
    config.read(config_path, encoding="utf-8")
    flag = 0
    sections = config.sections()
    print("共有%d个监控项，%s" % (len(config.sections()) - 2, sections))
    header = json.loads(config['account']['header'])
    cookie = json.loads(config['account']['ck'])
    print("载入用户：%s" % (cookie["ngaPassportUrlencodedUname"]))
    corp_id = json.loads(config['wechat']['corp_id'])
    corp_secret = json.loads(config['wechat']['corp_secret'])
    agent_id = json.loads(config['wechat']['agent_id'])
    # for each in sections:
    #     if "target" in each:
    #         print(config[each]['name'] + "线程开始")
    #         t = threading.Thread(target= test(), args=())
    #         t.start()
    #         # print(config[each])
    #         # get_page()
    #         # break
    tmp = []
    thread_list = []
    for each in sections:
        if "keywords" in each:
            tmp.append(each)
    for i in range(len(tmp)):
        print(config[tmp[i]]['name'] + "线程开始")
        t = threading.Thread(target=get_page, args=(tmp[i], i,))
        thread_list.append(t)
        # time.sleep(5)
    for t in thread_list:
        t.setDaemon(True)
        t.start()
        # print(config[each])
        # get_page()
        # break
    for t in thread_list:
        t.join()  # 子线程全部加入，主线程等所有子线程运行完毕
    elapsed = (time.time() - op)
    print('-------用时：{}'.format(elapsed) + '-------')