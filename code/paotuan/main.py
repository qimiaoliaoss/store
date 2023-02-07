# -*- coding: utf-8 -*-
# @Time : 2023/2/6 16:13
# @Author : Losir
# @FileName: main.py
# @Software: PyCharm
import random
import time
import sys


def fight():
    roll = random.randint(1, 6)
    print("命运之骰掷出了一个%d" % roll)


def player():
    global job, hp, att, mp
    job = input("选择一个职业：\n1、战士(血量攻击力加成，大幅削减魔力)\n2、法师(魔力加成，大幅削减近战攻击，略微脆皮)\n3、无用之人(白板，0分卡)\n")
    print('正在生成人物属性')
    if job == '1':
        # print("战士开局")
        hp = 120
        att = random.randint(10, 20)
        mp = 80
        if att <= 13:
            print('你的运气有够叼差的，下次Roll属性前记得洗洗手嗷，你这攻击力很弱诶')
        elif att == 20:
            print('运气爆表！攻击力被你Roll满了！')
    elif job == '2':
        # print("法师开局")
        hp = 80
        att = 4
        mp = random.randint(100, 120)
        if mp <= 105:
            print('你的运气有够叼差的，下次Roll属性前记得洗洗手嗷，你这法力值够都不看的啦，有够弱的齁')
        elif mp == 120:
            print('运气爆表！法力值被你Roll满了！')
    elif job == '3':
        print("无用开局")
    else:
        print("请输入规定数字")
    print("------------\n职业：%s\n生命值：%d\n魔力值：%d\n攻击力：%d\n------------" % (job_list[job], hp, mp, att))


def debug():
    print(41 // 10)
    exit()


if __name__ == "__main__":
    # debug()
    hp = 100
    mp = 100
    att = 10
    job = ''
    exp = 0
    floor = random.randint(1, 100)
    print('本次地牢共有%d层，祝你好运' % floor)
    job_list = {'1': "战士", '2': '法师', '3': '无用之人'}
    player()
