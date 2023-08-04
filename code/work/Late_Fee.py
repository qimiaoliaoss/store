# -*- coding: utf-8 -*-
# @Time : 2023/8/3 11:03
# @Author : Losir
# @FileName: Late_Fee.py
# @Software: PyCharm
# 计算滞纳金

from datetime import datetime, timedelta

current_date = datetime.now()
formatted_date = current_date.strftime("%Y-%m-%d")
flag = False

# 获取用户输入的日期和本金
dateInput = input("请输入日期（格式：YYYY-MM-DD）：")
principalInput = float(input("请输入本金："))
endDate_str = formatted_date

# 将日期字符串转换为datetime对象
startDate = datetime.strptime(dateInput, "%Y-%m-%d")
endDate = datetime.strptime(endDate_str, "%Y-%m-%d")

# 获取滞纳金率
lateFeeRate = float(input("请输入滞纳金率（例如：0.03 表示 3%）："))

# 计算日期差值
delta = endDate - startDate

# 获取间隔天数
interval_days = delta.days + 1

# 滞纳金上限，本金的100 %
maxLateFeeRate = 1.0

# 判断是否收取滞纳金
days = interval_days - 15
if days > 0:
    flag = True

print('开单日期：{}, 当前日期：{}, 本金：{}, 滞纳金率：{}, 是否计算滞纳金：{}'.format(startDate, endDate, principalInput, lateFeeRate, flag))

if flag:
    for i in range(1, days + 1):
        lateFee = principalInput * i * lateFeeRate
        lateFee = min(lateFee, principalInput * maxLateFeeRate)

        # 输出当天日期和滞纳金金额
        date_of_fee = startDate + timedelta(days=i + 14)
        print('{}: {}'.format(date_of_fee.strftime("%Y-%m-%d"), lateFee))

        # 如果滞纳金金额已经大于本金，则停止计算
        if lateFee >= principalInput:
            break
