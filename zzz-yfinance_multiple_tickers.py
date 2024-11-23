# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 10:03:55 2024

@author: demer
"""

import datetime as dt
import yfinance as yf
import pandas as pd

stocks = ["AMZN", "MSFT", "INTC", "GOOG", "INFY.NS", "3988.HK"]
start = dt.datetime.today()-dt.timedelta(360)
end = dt.datetime.today()
cl_price = pd.DataFrame()
ohlcv_data = {}

for ticker in stocks:
    yf_data = yf.download(ticker, start, end)
    ohlcv_data[ticker] = yf_data
    adj_close = yf_data["Adj Close"]
    cl_price[ticker] = adj_close

ohlcv_data["MSFT"]["Open"]