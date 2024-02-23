# -*- coding: utf-8 -*-
# @Time : 2024/2/22 10:28
# @Author : Losir
# @FileName: yili_total.py
# @Software: PyCharm
import os
import re
import io
import glob
import time
import sys
from decimal import Decimal
enable_notification = 1   #0不发送通知   1发送通知
# 只有在需要发送通知时才尝试导入notify模块
if enable_notification == 1:
    try:
        from notify import send
    except ModuleNotFoundError:
        print("警告：未找到notify.py模块。它不是一个依赖项，请勿错误安装。程序将退出。")
        sys.exit(1)

class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for file in self.files:
            file.write(obj)
            file.flush()

    def flush(self):
        for file in self.files:
            file.flush()


# 获取当前工作目录
current_directory = os.getcwd()

# 获取当前目录的父目录
parent_directory = os.path.dirname(current_directory)
print(f"父目录: {parent_directory}")

# 假设我们要找的兄弟目录的名称是 "project2"
sibling_directory_name = "project2"

# 构建兄弟目录的路径
sibling_directory_path = os.path.join(parent_directory, sibling_directory_name)
print(f"兄弟目录路径: {sibling_directory_path}")

# 获取当前日期，例如：'2024-02-21'
current_date = time.strftime('%Y-%m-%d', time.localtime())
current_date = '2024-02-21'

# 构建日志文件名模式
log_file_pattern = os.path.join(sibling_directory_path, f"{current_date}-*.log")
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


captured_output = io.StringIO()
original_stdout = sys.stdout
sys.stdout = Tee(sys.stdout, captured_output)

# 输出每个账号的红包总额
if red_packet_totals:
    all_red = 0
    for account, total in red_packet_totals.items():
        print(f'账号 {account} 总共获得了 {total} 元现金红包')
        all_red += total
    print(f'{current_date} 共收入 {all_red} 元现金红包')
else:
    print(f'{current_date}统计失败，请检查脚本运行状态')

sys.stdout = original_stdout
output_content = captured_output.getvalue()
captured_output.close()

if enable_notification == 1:
    send("伊利红包统计 通知", output_content)

