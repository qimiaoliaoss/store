# -*- coding: utf-8 -*-
# @Time : 2024/7/17 15:46
# @Author : Losir
# @FileName: main.py
# @Software: PyCharm
# -*- coding: utf-8 -*-


import akshare as ak
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import requests


def fetch_fund_data():
    """Fetch and process data from Akshare."""

    def fetch_lof_spot():
        return ak.fund_lof_spot_em()

    def fetch_value_estimation():
        return ak.fund_value_estimation_em()

    def fetch_purchase_info():
        return ak.fund_purchase_em().drop(columns=["序号", "基金简称"])

    with ThreadPoolExecutor() as executor:
        lof_future = executor.submit(fetch_lof_spot)
        value_estimation_future = executor.submit(fetch_value_estimation)
        purchase_info_future = executor.submit(fetch_purchase_info)

        fund_lof_spot_df = lof_future.result()
        fund_value_estimation_df = value_estimation_future.result()
        fund_purchase_df = purchase_info_future.result()

    fund_lof_spot_df = fund_lof_spot_df.reset_index()[['代码', '最新价', '成交额', '涨跌幅', '换手率']]
    lof_list = fund_lof_spot_df["代码"].values

    fund_value_estimation_df = fund_value_estimation_df[fund_value_estimation_df['基金代码'].isin(lof_list)]
    fund_value_estimation_df = fund_value_estimation_df.drop(fund_value_estimation_df.columns[[0, 4, 5, 6, 7, 8]],
                                                             axis=1)
    fund_value_estimation_df = fund_value_estimation_df.rename(columns={fund_value_estimation_df.columns[2]: '估值'})

    result_df = pd.merge(fund_value_estimation_df, fund_lof_spot_df, left_on='基金代码', right_on='代码', how='left')
    result_df = result_df.drop(columns=['代码'])
    result_df = pd.merge(result_df, fund_purchase_df, on='基金代码', how='left')

    return result_df


def preprocess_data(df):
    """Preprocess the fetched data."""

    df = df.replace('---', np.nan)
    df['估值'] = df['估值'].astype(float)
    df['最新价'] = df['最新价'].astype(float)
    df['成交额'] = df['成交额'].fillna(0).astype(int)
    df['涨跌幅'] = df['涨跌幅'].astype(float)
    df['换手率'] = df['换手率'].astype(float)
    df['最新净值'] = df['最新净值/万份收益'].astype(float)
    df['购买起点'] = df['购买起点'].astype(int)
    df['日累计限定金额'] = df['日累计限定金额'].astype('int64')
    df['手续费'] = df['手续费'].astype(float)

    return df


def calculate_premium_rate(df):
    """Calculate the premium rate for the funds."""

    def calc_rate(row):
        if pd.notnull(row['估值']):
            return row['最新价'] / row['估值'] - 1
        else:
            return row['最新价'] / row['最新净值'] - 1

    df['溢价率'] = df.apply(calc_rate, axis=1) * 100
    df['溢价率'] = df['溢价率'].round(2)
    df['溢价率abs'] = abs(df['溢价率'])

    return df


def calculate_arbitrage_profit(df):
    """Calculate the potential arbitrage profit."""
    def calc_profit(row):
        # print(row)
        # 使用基金的限额作为交易金额
        # trade_amount = min(row['限额'], 100000)  # 假设限额和一个最大值（如100,000）取较小值
        trade_amount = row['日累计限定金额']    #直接与限额挂钩
        if row['溢价率'] >= 0:
            # 场内卖出盈利
            profit = trade_amount * row['溢价率'] / 100 - row['手续费'] * trade_amount / 100
        else:
            # 场内买入盈利
            profit = -trade_amount * row['溢价率'] / 100 - row['手续费'] * trade_amount / 100
        return profit

    df['套利利润'] = df.apply(calc_profit, axis=1).round(2)
    return df


def filter_funds(df):
    """Filter funds based on trading volume and premium rate criteria."""
    df = df[df["成交额"] >= 500000]
    # df = df[((df["溢价率"] >= 0.3) & (df["申购状态"] != "暂停申购")) |
    #         ((df["溢价率"] <= -0.7) & (df["赎回状态"] != "暂停赎回"))]
    df = df[((df["溢价率"] >= 3) & (df["申购状态"] != "暂停申购"))    |
            ((df["溢价率"] <= -3) & (df["赎回状态"] != "暂停赎回"))]
    df = calculate_arbitrage_profit(df)
    return df


def format_dataframe(df):
    """Format the dataframe columns and order."""
    df = df.sort_values(by='溢价率abs', ascending=False)
    new_column_order = [
        '基金代码', '基金名称', '溢价率', '成交额', '日累计限定金额', '换手率',
        '手续费', '申购状态', '赎回状态', '最新价', '最新净值/万份收益', '估值',
        '购买起点', '涨跌幅', '基金类型', '最新净值/万份收益-报告时间',
        '最新净值', '下一开放日', '溢价率abs', '套利利润'
    ]
    df = df.reindex(columns=new_column_order)
    df = df.drop(columns=['购买起点', '下一开放日', '溢价率abs', '最新净值/万份收益'])
    df = df.rename(columns={'最新净值/万份收益-报告时间': '净值日期', '日累计限定金额': '限额'})

    return df

def format_dataframe_to_string(df):
    """Format the dataframe columns and order, and convert to string with new lines."""
    df = df.sort_values(by='溢价率abs', ascending=False)
    new_column_order = [
        '基金代码', '基金名称', '溢价率', '成交额', '日累计限定金额', '换手率',
        '手续费', '申购状态', '赎回状态', '最新价', '最新净值/万份收益', '估值',
        '购买起点', '涨跌幅', '基金类型', '最新净值/万份收益-报告时间',
        '最新净值', '下一开放日', '溢价率abs', '套利利润'
    ]
    df = df.reindex(columns=new_column_order)
    df = df.drop(columns=['购买起点', '下一开放日', '溢价率abs', '最新净值/万份收益'])
    df = df.rename(columns={'最新净值/万份收益-报告时间': '净值日期', '日累计限定金额': '限额'})

    rows = []
    for _, row in df.iterrows():
        formatted_row = "\n".join([f"{col}：{row[col]}" for col in df.columns])
        rows.append(formatted_row)

    return "\n\n".join(rows)


def notify(content):
    token = ""  # 替换成你自己的token
    chat_id =   # 替换成你自己的chat_id
    chat_id_2 =
    r = requests.post(f'https:///bot{token}/sendMessage',
                      json={"chat_id": chat_id, "text": f"{content}"})
    r2 = requests.post(f'https:///bot{token}/sendMessage',
                      json={"chat_id": chat_id_2, "text": f"{content}"})
    # print(r.json())

def main():
    """Main function to fetch, process, and display fund data."""
    # Fetch and process data
    result_df = fetch_fund_data()
    result_df = preprocess_data(result_df)
    result_df = calculate_premium_rate(result_df)
    result_df = filter_funds(result_df)
    result_df = format_dataframe_to_string(result_df)
    result_df = f'套利监控\n\n{result_df}\n\n⚠️ 预测利润说明：\n\n\t- 本文中的预测利润数值与基金的日累计限定金额挂钩，并通过自动计算得出。请注意，计算结果不保证其正确性，且未扣除证券账户手续费。\n\t- 计算结果仅供参考，不代表实际收益。\n\n⚠️ 市场有风险，投资需谨慎。\n\n免责申明：\n\n\t- 本文所用数据来源于网络，旨在提供一般参考信息。\n\t- 使用者应自行核实相关信息，并独立判断投资决策。\n\t- 使用本文内容过程中所产生的任何风险和责任，由使用者自行承担。\n\t- 本文作者及发布者不对因使用本文内容而导致的任何直接或间接损失负责。\n'
    print(result_df)
    notify(result_df)


# Run the main function
if __name__ == '__main__':
    main()
