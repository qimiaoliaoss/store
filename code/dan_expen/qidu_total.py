# -*- coding: utf-8 -*-
# @Time : 2024/4/2 10:03
# @Author : Losir
# @FileName: qidu_total.py
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
# current_directory = os.getcwd()
current_directory = r'/ql/data/log/dan_七读小说_7/'

# 获取当前日期，例如：'2024-02-21'
current_date = time.strftime('%Y-%m-%d', time.localtime())
# current_date = '2024-04-10'

# 构建日志文件名模式
log_file_pattern = os.path.join(current_directory, f"{current_date}-15*.log")
print("文件路径:{}".format(log_file_pattern))

# 使用 glob 模块获取所有符合模式的日志文件
log_files = glob.glob(log_file_pattern)
if log_files:
    print("匹配到日志")
else:
    print("无当前日期日志")
# 使用正则表达式来提取账号编号和红包金额
# 小主 [4] 签到成功
pattern = r"小主 \[(\d+)\] (签到成功)"

# 使用字典来统计每个账号的红包总金额
red_packet_totals = {}

captured_output = io.StringIO()
original_stdout = sys.stdout
sys.stdout = Tee(sys.stdout, captured_output)

# 遍历每个日志文件
for log_file in log_files:
    with open(log_file, 'r', encoding='utf-8') as file:
        log_content = file.read()
        matches = re.findall(r"小主 \[(\d+)\] (签到成功)", log_content)
        if matches:
            for match in matches:
                account = match[0]
                status = match[1]
                print(f"账号 {account}: {current_date}{status}")
        else:
            print("未找到匹配的内容")

sys.stdout = original_stdout
output_content = captured_output.getvalue()
captured_output.close()

if enable_notification == 1:
    send("七读签到 通知", output_content)