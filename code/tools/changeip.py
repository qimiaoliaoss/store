# -*- coding: utf-8 -*-
# @Time : 2024/5/29 14:35
# @Author : Losir
# @FileName: changeip.py
# @Software: PyCharm
import requests
import re
import sys
import os


# 加载通知
def load_send():
    global send
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    if os.path.exists(cur_path + "/sendNotify.py"):
        try:
            pass
            from sendNotify import send
        except:
            send=False
            print(">>>加载通知服务失败~")
    else:
        send=False
        print(">>>加载通知服务失败~")
load_send()


# 假设这是你用来获取当前IP地址的函数
def get_current_ip(msg):
    # 置空IP地址
    ip = ""

    # 尝试使用3322.org网站获取公网IP
    try:
        url = "http://members.3322.org/dyndns/getip/"
        response = requests.get(url)
        ip = response.text.strip()
        print(f">>>使用3322.org获取公网IP成功：{ip}")
        msg = msg + "\n" + f">>>使用3322.org获取公网IP成功：{ip}"
    except requests.RequestException as e:
        print(">>>使用3322.org获取公网IP失败，尝试其他方式...")
        msg = msg + "\n" + ">>>使用3322.org获取公网IP失败，尝试其他方式..."

    # ip = ""

    # 尝试使用synology.com网站获取公网IP
    if not ip:
        url = "https://checkip.synology.com/"

        def get_external_ip():
            site = requests.get(url)
            grab = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', site.text)
            address = grab[0]
            return address

        ip = get_external_ip()
        if not ip:
            print(">>>使用synology.com获取公网IP失败，尝试其他方式...")
            msg = msg + "\n" + ">>>使用synology.com获取公网IP失败，尝试其他方式..."
        else:
            print(f">>>使用synology.com获取公网IP成功：{ip}")
            msg = msg + "\n" + f">>>使用synology.com获取公网IP成功：{ip}"

    # ip = ""

    # 尝试使用httpbin.org网站获取公网IP
    if not ip:
        try:
            url = "http://httpbin.org/ip"
            response = requests.get(url)
            data = response.json()
            ip = data['origin']
            print(f">>>使用httpbin.org获取公网IP成功：{ip}")
            msg = msg + "\n" + f">>>使用httpbin.org获取公网IP成功：{ip}"
        except requests.RequestException as e:
            print(">>>使用httpbin.org获取公网IP失败，请检查网络连接或其他问题。")
            msg = msg + "\n" + ">>>使用httpbin.org获取公网IP失败，请检查网络连接或其他问题。"

    # ip = ""

    # 判断是否获取到公网IP
    if not ip:
        print(">>>未获取到公网IP，过程终止...")
        msg = msg + "\n" + ">>>未获取到公网IP，过程终止..."
        return None, msg
    else:
        print(f">>>获取到公网IP：{ip}")
        return ip, msg


def main():
    msg = ">>>开始执行……"
    # 文件路径
    file_path = './david_cookies.js'

    # 获取当前IP地址
    current_ip, msg = get_current_ip(msg)

    if current_ip is not None:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        # 使用正则表达式提取文件中的所有IP地址
        ips_in_file = re.findall(r'(\d+\.\d+\.\d+\.\d+):\d+', file_content)

        # 初始化一个标记，检查是否有任何IP被替换
        ip_replaced = False

        # 遍历所有找到的IP地址
        for file_ip in ips_in_file:
            # 检查当前IP地址和文件中的IP地址是否一致
            if current_ip != file_ip:
                # 使用当前IP地址替换文件中的IP地址
                file_content = re.sub(rf'{file_ip}(:\d+)', rf'{current_ip}\1', file_content)
                ip_replaced = True

        # 如果有任何IP地址被替换，则写回文件
        if ip_replaced:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(file_content)
            print(f">>>所有旧IP地址已替换为 {current_ip}。")
            msg = msg + "\n" + ">>>所有旧IP地址已替换为 {current_ip}。"
        else:
            print(">>>当前IP地址和文件中的所有IP地址一致，无需替换。")
            msg = msg + "\n" + ">>>当前IP地址和文件中的所有IP地址一致，无需替换。"
        msg = msg + "\n" + ">>>执行结束……"
        send("公网IP检测\n\n" + msg + "\n", "本通知 by Losir")


if __name__ == "__main__":
    main()
