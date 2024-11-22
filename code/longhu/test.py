# -*- coding: utf-8 -*-
# @Time : 2024/7/15 16:53
# @Author : Losir
# @FileName: test.py
# @Software: PyCharm
import tushare as ts
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 设置Tushare的API token
ts.set_token('')
pro = ts.pro_api()

# 获取股票列表
stock_basic = pro.stock_basic(exchange='', list_status='L', fields='ts_code,name,area,industry,list_date')


# 过滤出一年内不是特殊情况的股票
def filter_stocks():
    # 获取当前日期和一年前的日期
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')

    # 排除ST、*ST、退市以及累计超过10天停盘的股票
    non_st_stocks = stock_basic[~stock_basic['name'].str.contains('ST')]

    eligible_stocks = []
    for ts_code in non_st_stocks['ts_code']:
        daily = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)

        # 检查累计停盘天数，通过成交量vol是否为0来确定停盘
        suspended_days = daily[daily['vol'] == 0].shape[0]
        if suspended_days <= 10:
            eligible_stocks.append(ts_code)

    return eligible_stocks


# 计算分位值并选股
def calculate_percentiles_and_select_stocks(stocks):
    selected_stocks = []

    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')

    for ts_code in stocks:
        valuation = pro.daily_basic(ts_code=ts_code, start_date=start_date, end_date=end_date,
                                    fields='trade_date,pe_ttm,pb,ps_ttm')

        # 计算每一天的分位值
        valuation = valuation.dropna()  # 删除缺失值的行
        if len(valuation) == 0:
            continue  # 如果没有有效数据，跳过

        pe_percentiles = valuation['pe_ttm'].rank(pct=True)
        pb_percentiles = valuation['pb'].rank(pct=True)
        ps_percentiles = valuation['ps_ttm'].rank(pct=True)

        # 找到分位值同时小于3%的股票
        if ((pe_percentiles < 0.03) & (pb_percentiles < 0.03) & (ps_percentiles < 0.03)).any():
            selected_stocks.append(ts_code)

    return selected_stocks


# 主函数
def main():
    eligible_stocks = filter_stocks()
    selected_stocks = calculate_percentiles_and_select_stocks(eligible_stocks)
    print("选中的股票：", selected_stocks)


if __name__ == "__main__":
    main()
