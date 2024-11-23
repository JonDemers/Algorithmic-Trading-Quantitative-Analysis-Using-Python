# -*- coding: utf-8 -*-
"""

Renko: Renko Chart

Time on X is not constant, price movement on Y is constant UP or DOWN

"""

import datetime as dt
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from stocktrends import Renko

stocks = ["AMZN", "GOOG", "MSFT"]
ohlcv_data = {}
hour_data = {}
renko_data = {}

for ticker in stocks:
    data = yf.download(ticker, period="1mo", interval="5m")
    data = data.dropna(how="any")
    ohlcv_data[ticker] = data
    data = yf.download(ticker, period="1y", interval="1h")
    data = data.dropna(how="any")
    hour_data[ticker] = data

def atr(df, n=14):
    df =  df.copy()
    df["H-L"] = df["High"] - df["Low"]
    df["H-PC"] = abs(df["High"] - df["Adj Close"].shift(1))
    df["L-PC"] = abs(df["Low"] - df["Adj Close"].shift(1))
    df["TR"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1, skipna=False)
    df["ATR"] = df["TR"].ewm(com=n, min_periods=n).mean()
    return df["ATR"]

def renko_df(df, hourly_df):
    df = df.copy()
    df.reset_index(inplace=True)
    df.drop("Close", axis=1, inplace=True)
    df.columns = ["date", "open", "high", "low", "close", "volume"]
    df2 = Renko(df)
    df2.brick_size = 3 * round(atr(hourly_df, 120).iloc[-1], 0)
    renko_df = df2.get_ohlc_data() #if using older version of the library please use get_bricks() instead
    return renko_df

for ticker in ohlcv_data:
    renko_data[ticker] = renko_df(ohlcv_data[ticker], hour_data[ticker])