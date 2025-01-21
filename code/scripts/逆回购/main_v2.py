# -*- coding: utf-8 -*-
# @Time : 2025/1/17 10:33
# @Author : Losir
# @FileName: main_v2.py
# @Software: PyCharm
"""
V2版本：改为使用配置文件读取各设定，并读取历史逆回购数据（包含开盘、收盘、最高、最低）综合进行期望计算
"""
import json
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import requests
import time
import chinese_calendar
import tushare as ts

# 从配置文件读取配置
def load_config(config_file='config.json'):
    """读取配置文件"""
    with open(config_file, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config

# 配置参数加载
config = load_config()
API_TOKEN = config["API_TOKEN"]
CODE_NAME = config["CODE_NAME"]
CHECK_DAYS = config["CHECK_DAYS"]
GUI_ON = config["GUI_ON"]
PRINCIPAL = config["PRINCIPAL"]
FEE_RATE = config["FEE_RATE"]
CSV_FILE_PATH = config["CSV_FILE_PATH"]

# 设置 Tushare API Token
ts.set_token(API_TOKEN)
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

def load_historical_data(file_path):
    """加载历史数据文件"""
    df = pd.read_csv(file_path)
    df['日期'] = pd.to_datetime(df['日期'], format='%Y%m%d')
    df = df.rename(columns={
        '日期': 'date', '开盘价': 'open', '收盘价': 'close',
        '最高价': 'high', '最低价': 'low', '成交额': 'turnover',
        '成交量': 'volume', '涨跌幅': 'change_pct', '涨跌额': 'change', '涨跌率': 'change_rate'
    })
    df = df.sort_values(by='date').set_index('date')
    return df

def calculate_expected_rate(df):
    """根据开盘价、最高价、最低价、收盘价计算期望利率和波动"""
    df['expected_rate'] = (df['open'] + df['close'] + df['high'] + df['low']) / 4
    df['volatility'] = df['high'] - df['low']
    mean_rate = df['expected_rate'].mean()
    std_rate = df['expected_rate'].std()
    return mean_rate, std_rate

def analyze_rates(df, trade_date, principal, fee_rate, ):
    """分析利率数据并给出建议"""
    mean_rate, std_rate = calculate_expected_rate(df)
    threshold = mean_rate + 1.5 * std_rate
    expect_rate = df['expected_rate'].iloc[-1]
    # current_rate = real_time_rate if real_time_rate else df['expected_rate'].iloc[-1]
    current_rate = get_real_time_rate()

    # 计算收益
    # days = 1  # 默认占用一天资金，可扩展为动态计算
    # gross_return = (principal * current_rate * days) / (365 * 100)
    # fee = principal * fee_rate
    # net_return = gross_return - fee
    net_return, gross_return, fee, days = calculate_return_with_holidays(principal, current_rate, trade_date, fee_rate)



    print("==== 国债逆回购利率分析V2 ====")
    print(f"近 {CHECK_DAYS} 天平均期望利率：{mean_rate:.2f}%")
    print(f"期望利率标准差：{std_rate:.2f}%")
    print(f"建议买入阈值：{threshold:.2f}%")
    print(f"当前期望利率：{expect_rate:.2f}%")
    if current_rate is not None:
        print(f"实时利率：{current_rate:.2f}%")
    else:
        print(f"实时利率：获取失败，建议自行查看")
    print(f"资金占用天数：{days} 天")
    print(f"理论万份收益：{gross_return:.2f} 元")
    print(f"手续费：{fee:.2f} 元")
    print(f"实际收益：{net_return:.2f} 元")

    if current_rate > threshold:
        suggestion = "当前期望利率较高，建议买入！"
    elif current_rate > mean_rate:
        suggestion = "当前期望利率较平均值略高，可以考虑买入。"
    else:
        suggestion = "当前期望利率较低，暂不买入。"

    print(f"买入建议：{suggestion}")
    return mean_rate, std_rate, threshold, suggestion

def visualize_rates(df):
    """可视化利率数据"""
    matplotlib.font_manager.fontManager.addfont('chinese.simhei.ttf')
    matplotlib.rc('font', family='SimHei')
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['expected_rate'], label="期望利率", color='blue')
    plt.fill_between(df.index, df['expected_rate'] - df['volatility'],
                     df['expected_rate'] + df['volatility'], color='blue', alpha=0.2, label="波动范围")
    plt.axhline(df['expected_rate'].mean(), color='green', linestyle='--', label="平均期望利率")
    plt.title("国债逆回购期望利率趋势")
    plt.xlabel("日期")
    plt.ylabel("利率 (%)")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

def main(file_path):
    df = load_historical_data(file_path)
    trade_date = datetime.now().strftime('%Y-%m-%d')
    mean_rate, std_rate, threshold, suggestion = analyze_rates(df, trade_date, principal=PRINCIPAL, fee_rate=FEE_RATE)
    if GUI_ON:
        visualize_rates(df)

if __name__ == "__main__":
    main(CSV_FILE_PATH)
