# -*- coding: utf-8 -*-
# @Time : 2024/11/22 11:03
# @Author : Losir
# @FileName: main.py
# @Software: PyCharm

import tushare as ts
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import requests
import time
import chinese_calendar

# 设置 Tushare API Token
ts.set_token("")

# 配置名称和参数
CODE_NAME = "GC001"
CHECK_DAYS = 180
GUI_ON = True
PRINCIPAL = 10000  # 本金（元）
FEE_RATE = 0.00001  # 手续费比例
pro = ts.pro_api()

def get_real_time_rate():
    """获取实时国债逆回购利率"""
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "hq.sinajs.cn",
        "Referer": "https://money.finance.sina.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }
    base_url = "https://hq.sinajs.cn/etag.php"
    list_param = "sh204001"
    timestamp = int(time.time() * 1000)
    url = f"{base_url}?_={timestamp}&list={list_param}"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200 and response.text != '':
            data = response.text.split('="')[1].rstrip('";')
            values = data.split(',')
            return float(values[3])
        else:
            raise ValueError("未找到利率数据，请检查页面结构。")
    except Exception as e:
        print(f"获取实时利率失败：{e}")
        return None

def calculate_return_with_holidays(principal, rate, trade_date, fee_rate):
    """
    计算资金占用天数和收益（考虑T+1规则、节假日、春节长假）
    """
    trade_date = datetime.strptime(trade_date, '%Y-%m-%d')

    if trade_date.weekday() in [5, 6]:
        raise ValueError("周六或周日不能进行国债逆回购交易！")

    # 确定T+1计息日
    settlement_date = trade_date + timedelta(days=1)
    while chinese_calendar.is_holiday(settlement_date) or settlement_date.weekday() in [5, 6]:
        settlement_date += timedelta(days=1)

    # 获取节假日信息
    holiday_start = None
    for i in range(10):  # 向后检查最多10天的假期开始
        check_date = trade_date + timedelta(days=i)
        if chinese_calendar.is_holiday(check_date) or check_date.weekday() in [5, 6]:
            holiday_start = check_date
            break

    if holiday_start:
        # 获取假期结束后的第一个工作日
        holiday_end = holiday_start
        while chinese_calendar.is_holiday(holiday_end) or holiday_end.weekday() in [5, 6]:
            holiday_end += timedelta(days=1)

        # 倒数第二个交易日处理
        last_working_day = holiday_start - timedelta(days=1)
        while chinese_calendar.is_holiday(last_working_day) or last_working_day.weekday() in [5, 6]:
            last_working_day -= timedelta(days=1)

        if trade_date == last_working_day - timedelta(days=1):
            # 如果是倒数第二个工作日
            settlement_date = last_working_day  # 假期前的最后一个工作日
            days = (holiday_end - settlement_date).days
        else:
            # 普通情况
            days = (holiday_end - settlement_date).days + 1
    else:
        # 非节假日情况
        days = 1

    # 计算收益
    gross_return = (principal * rate * days) / (365 * 100)
    fee = principal * fee_rate
    net_return = gross_return - fee

    return net_return, gross_return, fee, days



def fetch_historical_rates(code_name, start_date, end_date):
    """获取历史利率数据"""
    try:
        df = pro.shibor(on=code_name, start_date=start_date, end_date=end_date)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        df.sort_index(inplace=True)
        return df
    except Exception as e:
        print("数据获取失败，请检查 API Token 或网络连接")
        raise e

def analyze_rates(df, real_time_rate, principal, fee_rate, trade_date):
    """分析利率数据并给出建议"""
    mean_rate = df['on'].mean()
    std_rate = df['on'].std()
    threshold = mean_rate + 1.5 * std_rate

    current_rate = real_time_rate if real_time_rate else df['on'].iloc[-1]
    net_return, gross_return, fee, days = calculate_return_with_holidays(principal, current_rate, trade_date, fee_rate)

    print("==== 国债逆回购利率分析 ====")
    print(f"种类名称：{CODE_NAME}")
    print(f"近 {CHECK_DAYS} 天平均利率：{mean_rate:.2f}%")
    print(f"利率标准差：{std_rate:.2f}%")
    print(f"建议买入阈值：{threshold:.2f}%")
    print(f"当前利率：{current_rate:.2f}%")
    print(f"资金占用天数：{days} 天")
    print(f"理论万份收益：{gross_return:.2f} 元")
    print(f"手续费：{fee:.2f} 元")
    print(f"实际收益：{net_return:.2f} 元")

    if current_rate > threshold:
        suggestion = "当前利率较高，建议买入！"
    elif current_rate > mean_rate:
        suggestion = "当前利率较平均值略高，可以考虑买入。"
    else:
        suggestion = "当前利率较低，暂不买入。"

    print(f"买入建议：{suggestion}")
    return mean_rate, std_rate, threshold, suggestion

def visualize_rates(df, current_rate, mean_rate, threshold):
    """可视化利率数据"""
    matplotlib.font_manager.fontManager.addfont('chinese.simhei.ttf')
    matplotlib.rc('font', family='SimHei')
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['on'], label="历史利率", color='blue')
    plt.axhline(mean_rate, color='green', linestyle='--', label="平均利率")
    plt.axhline(threshold, color='red', linestyle='--', label="建议买入阈值")
    plt.scatter([df.index[-1]], [current_rate], color='orange', label="当前利率")
    plt.title("国债逆回购一天期利率趋势")
    plt.xlabel("日期")
    plt.ylabel("利率 (%)")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

def main():
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=CHECK_DAYS)).strftime('%Y%m%d')
    df = fetch_historical_rates(CODE_NAME, start_date, end_date)

    if df.empty:
        raise ValueError("未能获取到任何利率数据，请确认 API 设置或日期范围是否正确。")

    real_time_rate = get_real_time_rate()
    if real_time_rate is not None:
        print(f"实时利率：{real_time_rate:.2f}%")
    else:
        print("无法获取实时利率，将仅使用历史数据进行分析。")

    trade_date = datetime.now().strftime('%Y-%m-%d')
    mean_rate, std_rate, threshold, suggestion = analyze_rates(df, real_time_rate, PRINCIPAL, FEE_RATE, trade_date)

    if GUI_ON:
        visualize_rates(df, real_time_rate if real_time_rate else df['on'].iloc[-1], mean_rate, threshold)

if __name__ == "__main__":
    main()
