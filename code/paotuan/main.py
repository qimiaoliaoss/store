# -*- coding: utf-8 -*-
# @Time : 2023/2/6 16:13
# @Author : Losir
# @FileName: main.py
# @Software: PyCharm
import random
import time
import sys
from flask import Flask
# app = Flask(__name__)


def roll():
    roll_num = random.randint(1, 100)
    # print(roll_num)
    return roll_num


def judge():
    if roll() > 50:
        return True
    else:
        return False


def judge_crit():
    if roll() > 80:
        return True
    else:
        return False


def judge_skill():
    cast = random.randint(1, 6)
    if job == '1':
        if cast == 1 and roll() == 1:
            return cast
        elif cast == 2 and roll() <= 20:
            return cast
        elif cast == 3 and roll() <= 5:
            return cast
        elif cast == 4 and roll() <= 80:
            return cast
        elif cast == 5 and roll() <= 15:
            return cast
        elif cast == 6 and roll() <= 80:
            return cast
        else:
            return False
    elif job == '2':
        if cast == 1 and roll() <= 90:
            return cast
        elif cast == 2 and roll() <= 60:
            return cast
        elif cast == 3 and roll() <= 50:
            return cast
        elif cast == 4 and roll() <= 30:
            return cast
        elif cast == 5 and roll() <= 10:
            return cast
        elif cast == 6 and roll() <= 70:
            return cast
        else:
            return False
    else:
        return False


def judge_use_skill():
    global job, percent
    if job == '1':
        percent = 60
    elif job == '2':
        percent = 90
    else:
        return False
    if roll() <= percent:
        use_skill = judge_skill()
        return use_skill
    else:
        return False


def fight():
    roll_tmp = roll()
    print("命运之骰掷出了一个%d" % roll_tmp)
    if roll_tmp <= 50:
        print("运气不好，怪物先攻")
    else:
        print("你赢得了主动")
    return roll_tmp


def input_player():
    global job
    job = input("选择一个职业：\n1、战士(血量攻击力加成，大幅削减魔力)\n2、法师(魔力加成，大幅削减近战攻击，略微脆皮)\n3、无用之人(白板，0分卡)\n")


def player():
    global job, hp, hp_limit, att, mp, mp_limit, percent
    print('正在生成人物属性')
    if job == '1':
        # print("战士开局")
        hp_limit = 200
        hp = hp_limit
        att = random.randint(15, 25)
        mp_limit = 80
        mp = mp_limit
        if att <= 18:
            print('你的运气有够叼差的，下次Roll属性前记得洗洗手嗷，你这攻击力很弱诶')
        elif att == 25:
            print('运气爆表！攻击力被你Roll满了！')
    elif job == '2':
        # print("法师开局")
        hp_limit = 80
        hp = hp_limit
        att = random.randint(5, 12)
        mp_limit = random.randint(100, 120)
        mp = mp_limit
        if mp <= 105:
            print('你的运气有够叼差的，下次Roll属性前记得洗洗手嗷，你这法力值够都不看的啦，有够弱的齁')
        elif mp == 120:
            print('运气爆表！法力值被你Roll满了！')
    elif job == '3':
        hp = hp_limit
        mp = mp_limit
        print("无用开局")
    else:
        print("请输入规定数字")
        input_player()
    print("------------\n职业：%s\n生命值：%d/%d\n魔力值：%d/%d\n攻击力：%d\n------------" %
          (job_list[job], hp, hp_limit, mp, mp_limit, att))


def combat(mobs_hp):
    global floor, hp, hp_limit, mp, mp_limit, att, att_flag, mage_5_count
    skill_flag = judge_use_skill()
    # print(skill_flag)
    if skill_flag:
        if mp <= 0:
            print("没蓝还想发大招？笑嘻人了")
        # 战士技能检索
        elif job == '1' and skill_flag == 1 and mp // 65 != 0:
            mobs_hp = mobs_hp - mobs_hp
            mp -= 65
            print("运气爆表！你用出了传说技能%s，怪物血量直接掉至%d点，爆杀！剩余法力值%d" % (warrior_skill[skill_flag], mobs_hp, mp))
        elif job == '1' and skill_flag == 2 and mp // 40 != 0:
            if hp < 16:
                hp += 30
                att += 15
                mp -= 40
                print("你使用了技能%s，攻击力提升至%d，希望这能有用。剩余法力值%d" % (warrior_skill[skill_flag], att, mp))
            else:
                if hp + 10 <= hp_limit:
                    hp += 10
                    print("你本来想使用技能%s，但是你似乎还没把自己逼到绝境，浅回10血意思一下" % (warrior_skill[skill_flag]))
                else:
                    tmp = hp_limit - hp
                    hp = hp_limit
                    print("你本来想使用技能%s，但是你似乎还没把自己逼到绝境，浅回%d血意思一下" % (warrior_skill[skill_flag], tmp))
        elif job == '1' and skill_flag == 3 and mp // 80 != 0:
            tmp_cut_heal = random.randint(20, 40)
            hp -= tmp_cut_heal
            att += 30
            mp -= 80
            print("你使用了技能%s，攻击力提升至%d，但是因为失血过多你只剩下%d点血了。剩余法力值%d" %
                  (warrior_skill[skill_flag], att, hp, mp))
        elif job == '1' and skill_flag == 4 and mp // 20 != 0:
            tmp_cut_heal = random.randint(10, 20)
            if hp + tmp_cut_heal > hp_limit:
                hp = hp_limit
            else:
                hp += tmp_cut_heal
            mp -= 20
            print("你使用了技能%s，恢复了%d点生命值，现在你还有%d点血，剩余法力值%d" %
                  (warrior_skill[skill_flag], tmp_cut_heal, hp, mp))
        elif job == '1' and skill_flag == 5:
            tmp_mp_to_hp = mp / 2
            if hp + tmp_mp_to_hp > hp_limit:
                hp_limit = hp + tmp_mp_to_hp
                hp = hp_limit
                print("你发动了%s，清空了法力并将一半转换为鲜血，血量上限提升至%d，亏损这么多还桀桀的笑简直发癫，现在还有%d血" %
                      (warrior_skill[skill_flag], hp_limit, hp))
            else:
                hp += tmp_mp_to_hp
                print("你发动了%s，清空了法力并将一半转换为鲜血，亏损这么多还桀桀的笑简直发癫，现在还有%d血" %
                      (warrior_skill[skill_flag], hp))
            mp -= mp
        elif job == '1' and skill_flag == 6 and mp // 15 != 0:
            att_flag = False
            mp -= 15
            print("你发动了%s，会百分百住下次怪物的攻击，剩余法力值%d" %
                  (warrior_skill[skill_flag], mp))
        elif job == '1' and not skill_flag:
            print("你尝试搓技能，但你悟性不够啊笨逼，失败了呗")
        elif job == '1':
            print('你本来想用技能%s，但没蓝啦，快去补魔吧gogogo' % warrior_skill[skill_flag])
        # 法师技能检索
        elif job == '2' and skill_flag == 1 and mp // 5 != 0:
            att_cut = random.randint(15, 20)
            mobs_hp -= att_cut
            mp -= 5
            print("叽里咕噜，您用出了%s，点了一下造成了%d点伤害！剩余法力值%d" % (mage_skill[skill_flag], att_cut, mp))
        elif job == '2' and skill_flag == 2 and mp // 20 != 0:
            mobs_hp -= 30
            mp -= 20
            print("叽里咕噜，您用出了%s，造成了20点伤害！但是冰冻效果好像是个摆设？剩余法力值%d" % (mage_skill[skill_flag], mp))
        elif job == '2' and skill_flag == 3 and mp // 30 != 0:
            mobs_hp -= 45
            mp -= 30
            print("叽里咕噜，您用出了%s，造成了45点伤害！不过火焰效果我也妹写，剩余法力值%d" % (mage_skill[skill_flag], mp))
        elif job == '2' and skill_flag == 4 and mp // 80 != 0:
            mobs_hp -= mobs_hp
            mp -= 80
            print("叽里咕噜，您用出了%s！！！，直接把怪秒了，牛逼！剩余法力值%d" % (mage_skill[skill_flag], mp))
        elif job == '2' and skill_flag == 5 and mp // 80 != 0:
            mage_5_count = 3
            mp -= 80
            print("叽里咕噜，您用出了%s！！！，在接下来三个房间里的战斗将会拥有恢复生命值和增加攻击力的buff，剩余法力值%d" % (mage_skill[skill_flag], mp))
        elif job == '2' and skill_flag == 6:
            hp += 5
            if mp + 20 >= mp_limit:
                mp = mp_limit
            else:
                mp += 20
            print("你从百宝袋里掏出来了%s，生命值恢复至%d，法力值恢复至%d" % (mage_skill[skill_flag], hp, mp))
        elif job == '2' and not skill_flag:
            print("你尝试搓法术，但你上课不认真，失败了呗")
        elif job == '2':
            print('你本来想用技能%s，但没蓝啦，快去补魔吧gogogo' % mage_skill[skill_flag])
    elif judge_crit():
        mobs_hp = mobs_hp - 2 * att
        print("你对怪物造成了%d点暴击伤害(怪物剩%d血)" % (2 * att, mobs_hp))
    else:
        mobs_hp = mobs_hp - att
        print("你对怪物造成了%d点伤害(怪物剩%d血)" % (att, mobs_hp))
    return mobs_hp


def mobs_combat(mobs_att):
    global hp, att_flag
    if att_flag:
        if judge_crit():
            hp = hp - 2 * mobs_att
            print("怪物对你造成了%d点暴击伤害(你还有%d血)" % (2 * mobs_att, hp))
        else:
            hp = hp - mobs_att
            print("怪物对你造成了%d点伤害(你还有%d血)" % (mobs_att, hp))
    else:
        print("格挡住了怪物的攻击")
        att_flag = True


def floors():
    global floor, hp, hp_limit, mp, att, mage_5_count
    now = 1
    kill = 0
    while now <= floor:
        mobs_num = random.randint(1, 10)
        boss_cut = random.randint(1, mobs_num)
        print("开始闯关第%d层，本层共有%d只怪，第%d个为Boss房，愿风指引你" % (now, mobs_num, boss_cut))
        for i in range(1, mobs_num + 1):
            if mage_5_count > 0:
                hp_mage_5_cut = random.randint(10, 30)
                att_mage_5_cut = random.randint(1, 3)
                hp += hp_mage_5_cut
                att += att_mage_5_cut
                mage_5_count -= 1
                print("触发了大治疗术的效果，生命值恢复%d点，攻击力上升%d点，buff效果还剩%d个房间" %
                      (hp_mage_5_cut, att_mage_5_cut, mage_5_count))
            if now < 11:
                span_level = 1
            else:
                span_level = now / 10
            if i != boss_cut:
                # mobs_level = random.randint(now // 10)
                mobs_hp = int(random.randint(20, 50) * span_level)
                mobs_mp = int(random.randint(20, 50) * span_level)
                mobs_att = int(random.randint(2, 6) * span_level)
                print("------------\n当前：小怪\n生命值：%d\n魔力值：%d\n攻击力：%d\n------------" %
                      (mobs_hp, mobs_mp, mobs_att))
            elif i == boss_cut:
                mobs_hp = int(random.randint(40, 60) * span_level)
                mobs_mp = int(random.randint(30, 60) * span_level)
                mobs_att = int(random.randint(6, 10) * span_level)
                print("------------\n当前：BOSS房\n生命值：%d\n魔力值：%d\n攻击力：%d\n------------" %
                      (mobs_hp, mobs_mp, mobs_att))
            print("开始战斗")
            roll_tmp = fight()
            while hp > 0 and mobs_hp > 0:
                # 怪物先攻
                if roll_tmp <= 50:
                    if judge():
                        # if judge_crit():
                        #     hp = hp - 2 * mobs_att
                        #     print("怪物对你造成了%d点暴击伤害(你还有%d血)" % (2 * mobs_att, hp))
                        # else:
                        #     hp = hp - mobs_att
                        #     print("怪物对你造成了%d点伤害(你还有%d血)" % (mobs_att, hp))
                        mobs_combat(mobs_att)
                    else:
                        print("他手滑了！对你miss！")
                    if judge():
                        mobs_hp = combat(mobs_hp)
                    else:
                        print("这你都打不中？")
                # 玩家先攻
                else:
                    if judge():
                        mobs_hp = combat(mobs_hp)
                    else:
                        print("这你都打不中？")
                    if judge():
                        # if judge_crit():
                        #     hp = hp - 2 * mobs_att
                        #     print("怪物对你造成了%d点暴击伤害(你还有%d血)" % (2 * mobs_att, hp))
                        # else:
                        #     hp = hp - mobs_att
                        #     print("怪物对你造成了%d点伤害(你还有%d血)" % (mobs_att, hp))
                        mobs_combat(mobs_att)
                    else:
                        print("他手滑了！对你miss！")
                time.sleep(1)
            if hp <= 0 and mobs_hp <= 0:
                print("------------\n惨烈，你在%d层这里就同归于尽了" % now)
                return now, kill
            elif hp <= 0:
                print("------------\n胜败乃是兵家常事，少侠下次再来")
                return now, kill
            elif mobs_hp <= 0:
                back_heal = random.randint(1, 10)
                back_mp = random.randint(1, 20)
                if job == '2':
                    back_heal = random.randint(1, 30)
                    back_mp = random.randint(1, 30)
                print("算你好运，通过一个，神秘力量为您回复%d点血量和%d点魔力" % (back_heal, back_mp))
                if hp + back_heal > hp_limit:
                    hp = hp_limit
                else:
                    hp += back_heal
                mp += back_mp
                kill += 1
                print("------------\n职业：%s\n生命值：%d/%d\n魔力值：%d/%d\n攻击力：%d\n------------" %
                      (job_list[job], hp, hp_limit, mp, mp_limit, att))
                # time.sleep(3)
        now += 1


def debug():
    print(100//10)
    exit()


def start():
    global hp, hp_limit, mp, mp_limit, att, job, exp, level, percent, job_list, warrior_skill, mage_skill, floor, att_flag, mage_5_count
    mage_5_count = 0
    hp_limit = 100
    mp_limit = 100
    att = 10
    job = ''
    exp = 0
    level = 1
    percent = 0
    att_flag = True
    floor = random.randint(1, 100)
    print('本次地牢共有%d层，祝你好运' % floor)
    job_list = {'1': "战士", '2': '法师', '3': '无用之人'}
    warrior_skill = {1: '枪出如龙', 2: '穷途末路', 3: '爆种', 4: '强身健体', 5: '饮魔', 6: '格挡'}
    mage_skill = {1: '火冲', 2: '寒冰箭', 3: '火球术', 4: '大字爆', 5: '大治疗术', 6: '法力之泉'}
    input_player()
    player()
    pass_floors, kill_mobs = floors()
    print("本次共闯过%d层，击杀%d只跟你同样有爹有妈的生物，欢迎下次再来" % (pass_floors, kill_mobs))
    return


if __name__ == "__main__":
    global hp, hp_limit, mp, mp_limit, att, job, exp, level, percent, job_list, warrior_skill, mage_skill, floor, att_flag, mage_5_count
    start()