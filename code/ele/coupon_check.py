# -*- coding: utf-8 -*-
# @Time : 2023/9/20 17:01
# @Author : Losir
# @FileName: coupon_check.py
# @Software: PyCharm
import re
import datetime
from notify import serverJ

# 账号对应关系，字典类型
data = {
    '158123456789': '张三',
}

def read_log(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"读取日志文件时出错：{e}")
        return None

def main():
    # 生成今天日期的文件名
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    file_path = 'log文件路径'
    log_text = read_log(file_path)

    if log_text:
        succ = []
        content = ''
        title = ''

        # 使用正则表达式进行文本拆分
        paragraphs = re.split(r'拆分界限', log_text)

        # 去除空白段落
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        # 打印拆分后的段落
        for i, paragraph in enumerate(paragraphs, 1):
            if '抢券成功' in paragraph:
                reg = '\*{6,} #1 (\d+) \*{6,}'
                phone = re.findall(reg, paragraph)
                if phone:
                    phone = phone[0]
                    succ.append(phone)

        if succ:
            count = len(succ)
            title = f'{today}入账{count}张'

            for each in succ:
                if each in data:
                    text_send = f'{each}({data[each]})抢券成功'
                    print(text_send)
                    content += f'{each}({data[each]})抢券成功\n'
                else:
                    print(f'未找到 {each} 对应的姓名')

        else:
            title = f'{today}空军'

        serverJ(title, content)

if __name__ == '__main__':
    main()


