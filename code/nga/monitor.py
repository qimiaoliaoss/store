# -*- coding: utf-8 -*-
# @Time : 2022/1/25 12:32
# @Author : Losir
# @FileName: kucun.py
# @Software: PyCharm

# 监控单一帖子内楼主回复

import configparser
import json
import os
import platform
import re
import threading
import time

import requests
from lxml import etree

# 获取操作环境
platform_sys = platform.system()
# 去除warning
requests.packages.urllib3.disable_warnings()


def get_proxy():
    return requests.get("https://proxy.ionssource.cn/get/").json()


def delete_proxy(proxy):
    requests.get("https://proxy.ionssource.cn/delete/?proxy={}".format(proxy))


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


def notify(new, tar):
    api = "https://sctapi.ftqq.com/SCT14710Tb1DiNZ09b0Wdg9wSh9DD6E2H.send"
    title = config[tar]['name'] + '新消息'
    content = new
    data = {
        "text": title,
        "desp": content
    }
    req = requests.post(api, headers=header, verify=False, timeout=10, data=data).content.decode('utf-8')
    print(req)


def get_page(tar, thread_num):
    try:
        flag = 0
        print('---------------------\n线程%d正在访问%s' % (thread_num, config[tar]["name"]))
        tid = config[tar]["tid"]
        uid = config[tar]["uid"]
        page = config[tar]["page"]
        last_time = config[tar]["time"]
        title = config[tar]["title"]
        url1 = "https://bbs.nga.cn/read.php?tid=" + tid + "&page=" + str(page)
        # print(url1)
        retry_count = 5
        proxy = get_proxy().get("proxy")
        open_code = '0'
        while retry_count > 0:
            try:
                res = requests.get(url1, headers=header, proxies={"http": "http://{}".format(proxy)}, verify=False
                                   , timeout=10, cookies=cookie)
                open_code = res.status_code
                print(open_code)
                break
            except Exception:
                if open_code == '503':
                    break
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
            m1 = re.compile(r"tid=" + tid + "',1:(.+?),")
            m3 = re.compile(r"<h1 class='x'>(.+?)</h1>")
            title = m3.findall(res_html)[0]
            print("---------------------\n帖子名称：" + title)
            # print(html.xpath('//*[@id="pagebbtm"]/script/text()'))
            try:
                end = m1.findall(html.xpath('//*[@id="pagebbtm"]/script/text()')[0])[0]
            except Exception:
                end = '1'
            config.set(tar, 'page', end)
            config.set(tar, 'title', title)
            config.write(open(config_path, "r+", encoding="utf-8"))
            new = ''
            print(config[tar]["name"] + "起始：" + page)
            print(config[tar]["name"] + "结束：" + end)
            for i in range(int(page), int(end) + 1):
                time.sleep(3)
                print(config[tar]["name"] + "第" + str(i) + "页")
                url = "https://bbs.nga.cn/read.php?tid=" + tid + "&page=" + str(i)
                res = requests.get(url, headers=header, verify=False, proxies={"http": "http://{}".format(proxy)},
                                   timeout=10, cookies=cookie)
                # print(res.status_code)
                if res.status_code == 200:
                    res = res.content.decode('GBK', errors='ignore')
                    html = etree.HTML(res)
                    m2 = re.compile(r"&uid=" + uid + "' id='(.+?)'")
                    id = m2.findall(res)
                    # print(id)
                    if id:
                        for j in range(len(id)):
                            id_tmp = id[j].replace("postauthor", "postcontent")
                            date = id_tmp.replace("postcontent", "postdate")
                            # print(id_tmp)
                            # print(date)
                            post_time = html.xpath('//*[@id="' + date + '"]/text()')[0]
                            print(config[tar]["name"] + post_time)
                            if post_time > last_time:
                                print("为新消息")
                                flag = 1
                                target = html.xpath('//*[@id="' + id_tmp + '"]/text()')
                                # print("发言内容：" + str(target))
                                target = str(target).replace("[img].", "https://img.nga.178.com/attachments")
                                target = str(target).replace("[/img]", " ")
                                target = eval(target)
                                rtarget = ''
                                for ttar in target:
                                    rtarget = rtarget + ttar + '\n'
                                new = new + "发言内容：\n" + rtarget + "\n\n发言时间：" + str(post_time) + "\n\n"
                                config.set(tar, 'time', post_time)
                                config.write(open(config_path, "r+", encoding="utf-8"))
                                print(new)
                else:
                    print("遍历%s发言错误，等待恢复" % config[tar]["name"])
                    if config[tar]['status'] == '200':
                        print("%s状态码%s" % (config[tar]["name"], config[tar]['status']))
                        config.set(tar, 'status', str(res.status_code))
                        config.write(open(config_path, "r+", encoding="utf-8"))
                        new = "遍历%s发言错误，等待恢复" % config[tar]["name"]
                        # flag = 1
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
        new = str(result)

    if flag == 1:
        notify(new, tar)


def test(tar, num):
    # print(config[tar])
    time.sleep(10)
    print("线程%d,%s开始睡觉" % (num, config[tar]['name']))


if __name__ == "__main__":
    op = time.time()
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    print('-------运行时间：{}'.format(now) + '-------')
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
        if "target" in each:
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
