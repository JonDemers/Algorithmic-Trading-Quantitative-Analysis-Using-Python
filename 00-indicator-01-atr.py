# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 10:03:55 2024

@author: demer

ATR: Average True Range

Measures market volatility
    High values: Market is volatile
    Low values: Market is stable

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


def atr(df, n=14):
    df =  df.copy()
    df["H-L"] = df["High"] - df["Low"]
    df["H-PC"] = abs(df["High"] - df["Adj Close"].shift(1))
    df["L-PC"] = abs(df["Low"] - df["Adj Close"].shift(1))
    df["TR"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1, skipna=False)
    df["ATR"] = df["TR"].ewm(com=n, min_periods=n).mean()
    return df["ATR"]

for ticker in ohlcv_data:
    df = ohlcv_data[ticker]
    df["ATR"] = atr(df)

    