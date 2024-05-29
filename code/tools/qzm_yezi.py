# -*- coding: utf-8 -*-
# @Time : 2024/4/28 15:35
# @Author : Losir
# @FileName: qzm.py
# @Software: PyCharm
import random
import time
import requests
import sys
import traceback


def get_balance(token):
    base_url = "http://api.sqhyw.net:90/api/get_myinfo"
    params = {"token": token}
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            balance = data["data"][0]["money"]
            return balance
        else:
            print("Failed to get balance. Status code:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None


def get_mobile(token, project_id, loop=None, operator=None, phone_num=None, scope=None, address=None,
               api_id=None, scope_black=None, creat_time=None):
    base_url = "http://api.sqhyw.net:90/api/get_mobile"
    params = {
        "token": token,
        "project_id": project_id,
        "loop": loop,
        "operator": operator,
        "phone_num": phone_num,
        "scope": scope,
        "address": address,
        "api_id": api_id,
        "scope_black": scope_black,
        "creat_time": creat_time
    }
    try:
        response = requests.get(base_url, params=params)
        # print(response.json())
        if response.status_code == 200:
            data = response.json()
            message = data["message"]
            if message == "ok":
                mobile = data["mobile"]
                remaining_attempts = data["1分钟内剩余取卡数:"]
                return mobile, remaining_attempts
            else:
                print("Failed to get mobile. Message:", message)
                return None, None
        else:
            print("Failed to get mobile. Status code:", response.status_code)
            return None, None
    except Exception as e:
        print("An error occurred:", e)
        return None, None


def free_mobile(token, project_id=None, special=None, phone_num=None):
    base_url = "http://api.sqhyw.net:90/api/free_mobile"
    params = {
        "token": token,
        # "project_id": project_id,
        # "special": special,
        "phone_num": phone_num
    }
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            message = data["message"]
            if message == "ok":
                print("号码释放成功.")
            else:
                print("Failed to release mobile number. Message:", message)
        else:
            print("Failed to release mobile number. Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", e)


def get_message(token, project_id, phone_num):
    base_url = "http://api.sqhyw.net:90/api/get_message"
    params = {
        "token": token,
        "project_id": project_id,
        "phone_num": phone_num,
    }
    try:
        start_time = time.time()
        print("等待短信中，等待时间：300s")
        while True:
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                # print(data)
                message = data["message"]
                if message != "ok":
                    current_time = time.time()
                    if current_time - start_time > 300:
                        print("300s未接收到验证码短信.")
                        return None, None, None, None
                    # print(message)
                    time.sleep(10)
                elif message == "ok":
                    if data["data"]:
                        code = data["code"]
                        modle = data["data"][0]["modle"]
                        project_id = data["data"][0]["project_id"]
                        project_type = data["data"][0]["project_type"]
                        return code, modle, project_id, project_type
                    else:
                        print("内容有误.")
                        print(data)
                        return None, None, None, None
            else:
                print("获取失败. 状态码:", response.status_code)
                return None, None, None, None
    except Exception as e:
        print("An error occurred:", e)
        return None, None, None, None


def login(username, password):
    base_url = "http://api.sqhyw.net:90/api/logins"
    params = {
        "username": username,
        "password": password
    }
    try:
        response = requests.get(base_url, params=params)
        # print(response.json())
        if response.status_code == 200:
            data = response.json()
            token = data["token"]
            user_data = data["data"][0]
            money = user_data["money"]
            user_id = user_data["id"]
            return token, money, user_id
        else:
            print("Failed to login. Status code:", response.status_code)
            return None, None, None
    except Exception as e:
        traceback.print_exc()
        print("An error occurred:", e)
        return None, None, None


def reg_sendsms(phone, relation):
    headers = {
        "Host": "api.quzanmi.com",
        "Connection": "keep-alive",
        "Content-Length": "30",
        "Accept": "application/json, text/plain, */*",
        "x-qzm-device": "android",
        "x-qzm-time": "1714293219",
        "x-qzm-aid": "undefined|undefined|undefined",
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; GM1900 Build/RKQ1.201022.002) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36",
        "x-qzm-bundle": "undefined|undefined|undefined|undefined",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "http://anh5.quzanmi.com",
        "X-Requested-With": "mark.via",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "http://anh5.quzanmi.com/landing?shifuId={}".format(relation),
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    data = {
        "phone_number": phone
    }

    # 发送请求
    # proxy = get_proxy().get("proxy")
    # xk_ip = xk_proxy()
    response = requests.post("https://api.quzanmi.com/api/open/sms/reg", json=data, headers=headers, proxies=proxies)

    # 处理响应
    if response.status_code == 200:
        json_response = response.json()
        if json_response.get("code") == 2000:
            print("邀请短信发送成功:", json_response.get("msg"))
            return True
            # 在这里处理请求成功后的逻辑
        else:
            print("邀请短信发送失败:", json_response.get("msg"))
            return False
            # 在这里处理请求失败后的逻辑
    else:
        print("邀请短信发送失败:", response.status_code)
        return False


def reg(smscode, phone, relation):
    import requests

    headers = {
        "Host": "api.quzanmi.com",
        "Connection": "keep-alive",
        "Content-Length": "66",
        "Accept": "application/json, text/plain, */*",
        "x-qzm-device": "android",
        "x-qzm-time": "1714293243",
        "x-qzm-aid": "undefined|undefined|undefined",
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; GM1900 Build/RKQ1.201022.002) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36",
        "x-qzm-bundle": "undefined|undefined|undefined|undefined",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "http://anh5.quzanmi.com",
        "X-Requested-With": "mark.via",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "http://anh5.quzanmi.com/landing?shifuId={}".format(relation),
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    data = {
        "code": smscode,
        "phone_number": phone,
        "relation": relation
    }

    # 发送请求
    # proxy = get_proxy().get("proxy")
    response = requests.post("https://api.quzanmi.com/api/user/info/reg", json=data, headers=headers, proxies=proxies)

    # 处理响应
    if response.status_code == 200:
        json_response = response.json()
        if json_response.get("code") == 2000:
            print("邀请成功:", json_response.get("msg"))
            return True
            # 在这里处理请求成功后的逻辑
        else:
            print("邀请失败:", json_response.get("msg"))
            return False
            # 在这里处理请求失败后的逻辑
    else:
        print("邀请失败:", response.status_code)
        return False


def login_sendsms(phone):
    headers = {
        "Host": "api.quzanmi.com",
        "Connection": "keep-alive",
        "Content-Length": "45",
        "x-qzm-time": "1714303379",
        "Origin": "http://anh5.quzanmi.com",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; MI 6 Build/PKQ1.190118.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 AgentWeb/5.0.8 UCBrowser/11.6.4.950",
        "x-qzm-bundle": "com.zhangwen.quzanmi|Xiaomi|9|1.0.1",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "x-qzm-device": "android",
        "x-qzm-aid": "|f03e3009a3f4671f|6a2252c80ef5f208",
        "Referer": "http://anh5.quzanmi.com/home",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "X-Requested-With": "com.zhangwen.quzanmi"
    }

    data = {
        "phone_number": phone,
        "kind": "login"
    }

    # 发送请求
    response = requests.post("https://api.quzanmi.com/api/open/sms/code", json=data, headers=headers, proxies=proxies)

    # 处理响应
    if response.status_code == 200:
        json_response = response.json()
        if json_response.get("code") == 2000:
            print("登录短信发送成功:", json_response.get("msg"))
            return True
            # 在这里处理请求成功后的逻辑
        else:
            print("登录短信发送失败:", json_response.get("msg"))
            return False
            # 在这里处理请求失败后的逻辑
    else:
        print("登录短信发送失败:", response.status_code)
        return False


def sms_login(smscode, phone):
    headers = {
        "Host": "api.quzanmi.com",
        "Connection": "keep-alive",
        "Content-Length": "58",
        "x-qzm-time": "1714301917",
        "Origin": "http://anh5.quzanmi.com",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; MI 6 Build/PKQ1.190118.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 AgentWeb/5.0.8 UCBrowser/11.6.4.950",
        "x-qzm-bundle": "com.zhangwen.quzanmi|Xiaomi|9|1.0.1",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "x-qzm-device": "android",
        "x-qzm-aid": "|f03e3009a3f4671f|6a2252c80ef5f208",
        "Referer": "http://anh5.quzanmi.com/home",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "X-Requested-With": "com.zhangwen.quzanmi"
    }

    data = {
        "phone_number": phone,
        "code": smscode,
        "relation": ""
    }

    # 发送请求
    response = requests.post("https://api.quzanmi.com/api/user/info/login", json=data, headers=headers, proxies=proxies)

    # 处理响应
    if response.status_code == 200:
        json_response = response.json()
        print(json_response)
        if json_response.get("code") == 2000:
            print("登录成功:", json_response.get("data").get("token"))
            return json_response.get("data").get("token")
            # 在这里处理登录频繁后的逻辑
        else:
            print("登陆失败:", json_response.get("msg"))
            # 在这里处理请求成功后的逻辑
    else:
        print("登陆失败:", response.status_code)


def test_login(token, project_id, phone):
    print('开始手动登录')
    mobile, remaining_attempts = get_mobile(token, project_id, phone_num=phone)
    if mobile is not None:
        # 发送登录短信
        if_success = login_sendsms(phone)
        if if_success:
            login_smscode, login_modle, login_project_id, login_project_type = get_message(token,
                                                                                           project_id,
                                                                                           phone)
        else:
            print('登陆短信发送失败')
            sys.exit()

        if login_smscode:
            print("验证码:", login_smscode)
            print("完整内容:", login_modle)
            token = sms_login(login_smscode, phone)
            with open("token.txt", "a") as file:
                file.write(phone + ' ' + token + "\n")
            print("Token写入成功")
        else:
            print('未收到注册短信，结束运行')


if __name__ == "__main__":
    # ----手动登录模块---- #
    # ----flag 1：启用---- #
    # ----修改手机号为登录号---- #
    flag = 0
    if flag == 1:
        confirm = input("即将进入手动流程，手动输入1进行二次确认：")
        if confirm == '1':
            proxies = {"http": "", "https": ""}
            project_id = ""
            token = ""
            phone = ''
            test_login(token, project_id, phone)
            sys.exit()
    # ----手动登录模块结束---- #
    for try_num in range(1, 11):
        # 登录阶段
        proxies = {"http": "", "https": ""}
        username = ""
        password = ""
        relation = ""
        token, money, user_id = login(username, password)
        if token is not None:
            balance = get_balance(token)
            if balance:
                print("余额:", balance)
            else:
                print("获取余额失败，请检查token.")
                sys.exit()
            # 取码阶段
            print("开始取码")
            project_id = ""
            # 限定实卡
            operator = "4"
            # 排除号段
            scope_black = "192"
            # 取接码号
            count = 1
            if_success = False
            while True:
                print('【{}】即将进行第{}次发码尝试'.format(try_num, count))
                mobile, remaining_attempts = get_mobile(token, project_id, operator=operator, scope_black=scope_black)
                if mobile:
                    print("【{}】接码号:{}".format(try_num, mobile))
                    print("【{}】1分钟内剩余取卡数:{}".format(try_num, remaining_attempts))
                    # phone = '1510000000'
                    # 发送注册短信
                    if_success = reg_sendsms(mobile,relation)
                else:
                    print('【{}】获取接码号失败'.format(try_num))
                    break
                if if_success:
                    break
                elif remaining_attempts == '200':
                    print('【{}】取码太长时间啦，晚点再试吧'.format(try_num))
                    break
                rti = random.randrange(30, 60)
                print('【{}】模拟睡眠{}秒'.format(try_num, rti))
                for j in range(rti, 0, -1):
                    print("\r【{}】倒计时{}秒！".format(try_num, j), end="", flush=True)
                    time.sleep(1)
                print("\r【{}】倒计时结束！".format(try_num))
                # time.sleep(rti)
                count += 1

            if if_success:
                smscode, modle, project_id, project_type = get_message(token, project_id, mobile)
            else:
                print('【{}】发送失败'.format(try_num))
                free_mobile(token, phone_num=mobile)
                continue

            if smscode is not None:
                print("【{}】验证码:{}".format(try_num, smscode))
                print("【{}】完整内容:{}".format(try_num, modle))
                # print("project_id:", project_id)
                # print("Project type:", project_type)
                if_reg = reg(smscode, mobile, relation)
            else:
                print('【{}】未收到邀请短信，结束运行'.format(try_num))
                continue

            # 登录阶段，若登陆失败注释以上内容至标识处，再修改以下两行尝试手动登录
            # if_reg = True
            # phone = 13000000000
            if if_reg:
                slept = random.randint(60, 120)
                for i in range(slept, 0, -1):
                    print("\r【{}】倒计时{}秒！".format(try_num, i), end="", flush=True)
                    time.sleep(1)
                print("\r【{}】倒计时结束！".format(try_num))
                get_mobile(token, project_id, phone_num=mobile)
                # 发送登录短信
                if_success = login_sendsms(mobile)
            else:
                print('【{}】邀请失败'.format(try_num))
                continue

            if if_success:
                login_smscode, login_modle, login_project_id, login_project_type = get_message(token,
                                                                                               project_id,
                                                                                               mobile)
            else:
                print('【{}】登陆短信发送失败'.format(try_num))
                continue

            if login_smscode:
                print("【{}】验证码:{}".format(try_num, login_smscode))
                print("【{}】完整内容:{}".format(try_num, login_modle))
                token = sms_login(login_smscode, mobile)
                if token:
                    with open("token.txt", "a") as file:
                        file.write(mobile + ' ' + token + "\n")
                    print("【{}】Token写入成功".format(try_num))
                else:
                    print('【{}】未收到登录短信，建议手动重试'.format(try_num))
                    with open("token.txt", "a") as file:
                        file.write(mobile + "\n")
                    print("【{}】号码写入成功".format(try_num))
            else:
                print('【{}】未收到登录短信，建议手动重试'.format(try_num))
                with open("token.txt", "a") as file:
                    file.write(mobile + "\n")
                print("【{}】号码写入成功".format(try_num))
