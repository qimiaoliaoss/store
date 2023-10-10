# -*- coding: utf-8 -*-
# @Time : 2023/10/10 16:39
# @Author : Losir
# @FileName: selfnotify.py.py
# @Software: PyCharm
import requests
import json
import os
import threading

push_config = {
    'corp_id': '',  # bark IP 或设备码，例：https://api.day.app/DxHcxxxxxRxxxxxxcm/
    'corp_secret': '',  # bark 推送是否存档
    'agent_id': '',  # bark 推送分组
}
notify_function = []

# 首先读取 面板变量 或者 github action 运行变量
for k in push_config:
    if os.getenv(k):
        v = os.getenv(k)
        push_config[k] = v


def get_access_token(corp_id, corp_secret):
    resp = requests.get(f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={corp_secret}')
    js = json.loads(resp.text)
    # print(js)
    if js["errcode"] == 0:
        access_token = js["access_token"]
        expires_in = js["expires_in"]
        return access_token, expires_in


def wechat_push_text(message: str) -> None:
    """
    使用 企业微信 推送消息。
    """
    if not push_config.get("corp_id") or not push_config.get("corp_secret") or not push_config.get("agent_id"):
        print("企业微信 服务的 corp_id 或者 corp_secret 或者 agent_id 未设置!!\n取消推送")
        return
    print("企业微信 服务启动")

    access_token, expires_in = get_access_token(push_config.get("corp_id"), push_config.get("corp_secret"))
    data = {
        "touser": "@all",
        "msgtype": 'text',
        "agentid": push_config.get("agent_id"),
        "text": {
            "content": message
        },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    resp = requests.post(f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}', json=data)
    js = json.loads(resp.text)
    # print(js)
    if js["errcode"] == 0:
        print("企业微信 推送成功！")
    else:
        print("企业微信 推送失败！")


def one() -> str:
    """
    获取一条一言。
    :return:
    """
    url = "https://v1.hitokoto.cn/"
    res = requests.get(url).json()
    return res["hitokoto"] + "    ----" + res["from"]


def send(title: str, content: str) -> None:
    if not content:
        print(f"{title} 推送内容为空！")
        return

    hitokoto = push_config.get("HITOKOTO")

    text = one() if hitokoto else ""
    content += "\n\n" + text

    ts = [
        threading.Thread(target=mode, args=(title, content), name=mode.__name__)
        for mode in notify_function
    ]
    [t.start() for t in ts]
    [t.join() for t in ts]


def main():
    send("title", "content")


if __name__ == "__main__":
    main()
