# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 10:03:55 2024

@author: demer

Bolling Band
    
Measures market volatility
    
Stock price moves between upper and lower bands

    MB: Middle Band
    UB: Upper Band
    LB: Lower Band
    BW: Band Width: small values means low volatility

"""

import datetime as dt
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

stocks = ["AMZN", "GOOG", "MSFT"]
ohlcv_data = {}

for ticker in stocks:
    data = yf.download(ticker, period="1mo", interval="5m")
    data = data.dropna(how="any")
    ohlcv_data[ticker] = data


def bolling_band(df, n=14):
    df =  df.copy()
    df_rolling = df["Adj Close"].rolling(n)
    df_rolling_mean = df_rolling.mean()
    df_rolling_2_std = 2*df_rolling.std(ddof=0)
    df["MB"] = df_rolling_mean
    df["UB"] = df_rolling_mean + df_rolling_2_std
    df["LB"] = df_rolling_mean - df_rolling_2_std
    df["BW"] = df["UB"] - df["LB"]
    return df[["MB","UB","LB","BW"]]

for ticker in ohlcv_data:
    df = ohlcv_data[ticker]
    df[["MB","UB","LB","BW"]] = bolling_band(df, n=20)


    