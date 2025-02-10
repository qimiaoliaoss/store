# -*- coding: utf-8 -*-
# @Time : 2025/1/17 11:22
# @Author : Losir
# @FileName: main_V3.py
# @Software: PyCharm
"""
V3版本：通过机器学习模型（在这里是线性回归模型）预测的未来利率值。我们基于历史数据训练模型，模型的目标是预测未来的期望利率。
优点：计算速度较快
缺点：模型绝对误差不够理想
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
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# 从配置文件读取配置
def load_config(config_file='F:/python/nga/code/scripts/逆回购/config.json'):
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

def load_historical_data(file_path):
    """加载历史数据文件"""
    df = pd.read_csv(file_path)
    df['日期'] = pd.to_datetime(df['日期'], format='%Y%m%d')
    df = df.rename(columns={ '日期': 'date', '开盘价': 'open', '收盘价': 'close',
                             '最高价': 'high', '最低价': 'low', '成交额': 'turnover',
                             '成交量': 'volume', '涨跌幅': 'change_pct', '涨跌额': 'change', '涨跌率': 'change_rate' })
    df = df.sort_values(by='date').set_index('date')
    return df

def calculate_expected_rate(df):
    """根据开盘价、最高价、最低价、收盘价计算期望利率"""
    df['expected_rate'] = (df['open'] + df['close'] + df['high'] + df['low']) / 4
    return df

def train_linear_regression_model(df):
    """使用线性回归模型训练预测期望利率"""
    df = calculate_expected_rate(df)

    # 选择合适的特征，这里用前几天的期望利率预测今天的期望利率
    df['lag_1'] = df['expected_rate'].shift(1)
    df['lag_2'] = df['expected_rate'].shift(2)
    df = df.dropna()  # 删除NaN值

    X = df[['lag_1', 'lag_2']]  # 特征：前两天的期望利率
    y = df['expected_rate']  # 目标变量：今天的期望利率

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = LinearRegression()
    model.fit(X_train, y_train)

    # 模型评估
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"模型平均绝对误差: {mae:.4f}")

    return model

def calculate_lag_features(df):
    """计算滞后特征"""
    df['lag_1'] = df['expected_rate'].shift(1)
    df['lag_2'] = df['expected_rate'].shift(2)
    df = df.dropna()  # 删除含NaN的行
    return df

def predict_expected_rate(model, df):
    """使用训练好的模型预测当前期望利率"""
    # 计算期望利率和滞后特征
    df = calculate_expected_rate(df)
    df = calculate_lag_features(df)

    # 取最后两天的数据用于预测
    last_two_days = df[['lag_1', 'lag_2']].tail(1)

    # 确保数据中有lag_1和lag_2
    if 'lag_1' not in last_two_days.columns or 'lag_2' not in last_two_days.columns:
        print("滞后特征丢失，无法进行预测")
        return None

    # 预测期望利率
    predicted_rate = model.predict(last_two_days)
    return predicted_rate[-1]

# 调用predict_expected_rate时，保证传入的DataFrame包含所有特征

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
    for i in range(2):  # 向后检查最多10天的假期开始
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

def analyze_rates(df, trade_date, principal, fee_rate, model):
    """分析利率数据并给出建议"""
    current_rate = get_real_time_rate()

    # 预测期望利率
    predicted_rate = predict_expected_rate(model, df)

    # 计算买入阈值
    threshold = predicted_rate + 1.5 * df['expected_rate'].std()

    # 计算收益
    net_return, gross_return, fee, days = calculate_return_with_holidays(principal, current_rate, trade_date, fee_rate)

    print("==== 国债逆回购利率分析V3 ====")
    print(f"预测期望利率：{predicted_rate:.2f}%")
    print(f"建议买入阈值：{threshold:.2f}%")
    print(f"当前实时利率：{current_rate:.3f}%")
    print(f"资金占用天数：{days} 天")
    print(f"理论万份收益：{gross_return:.2f} 元")
    print(f"手续费：{fee:.2f} 元")
    print(f"实际收益：{net_return:.2f} 元")

    if current_rate > threshold:
        suggestion = "当前期望利率较高，建议买入！"
    elif current_rate > predicted_rate:
        suggestion = "当前期望利率较平均值略高，可以考虑买入。"
    else:
        suggestion = "当前期望利率较低，暂不买入。"

    print(f"买入建议：{suggestion}")
    return predicted_rate, threshold, suggestion

def main(file_path):
    df = load_historical_data(file_path)
    model = train_linear_regression_model(df)
    trade_date = datetime.now().strftime('%Y-%m-%d')
    predicted_rate, threshold, suggestion = analyze_rates(df, trade_date, principal=PRINCIPAL, fee_rate=FEE_RATE, model=model)

if __name__ == "__main__":
    try:
        main(CSV_FILE_PATH)
    except Exception as e:
        print(f"程序发生错误: {e}")
