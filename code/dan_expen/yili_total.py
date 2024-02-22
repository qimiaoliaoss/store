# -*- coding: utf-8 -*-
# @Time : 2024/2/22 10:28
# @Author : Losir
# @FileName: yili_total.py
# @Software: PyCharm
import os
import re
import glob
import time
from decimal import Decimal


# 获取当前工作目录
current_directory = os.getcwd()

# 获取当前日期，例如：'2024-02-21'
current_date = time.strftime('%Y-%m-%d', time.localtime())
current_date = '2024-02-21'

# 构建日志文件名模式
log_file_pattern = os.path.join(current_directory, f"{current_date}-*.log")
print("文件路径:{}".format(log_file_pattern))

# 使用 glob 模块获取所有符合模式的日志文件
log_files = glob.glob(log_file_pattern)
if log_files:
    print("匹配到日志")
else:
    print("无当前日期日志")
# 使用正则表达式来提取账号编号和红包金额
pattern = r'【小主 \[(\d+)\] 】.*?获得([\d.]+)元现金红包'

# 使用字典来统计每个账号的红包总金额
red_packet_totals = {}

# 遍历每个日志文件
for log_file in log_files:
    with open(log_file, 'r', encoding='utf-8') as file:
        for line in file:
            # print(line)
            match = re.search(pattern, line)
            if match:
                account_number = match.group(1)
                red_packet_amount = Decimal(match.group(2))
                # print(f'账号 {account_number} 总共获得了 {red_packet_amount} 元现金红包')
                if account_number in red_packet_totals:
                    red_packet_totals[account_number] += red_packet_amount
                    # print(f'账号 {account_number} 总共获得了 {red_packet_amount} 元现金红包')
                else:
                    red_packet_totals[account_number] = red_packet_amount

# 输出每个账号的红包总额
for account, total in red_packet_totals.items():
    print(f'{current_date} 账号 {account} 总共获得了 {total} 元现金红包')

