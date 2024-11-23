# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 10:03:55 2024

@author: demer

MACD: Moving Average Convergence Divergence

Measure trend momentum and identify entry points for buying or selling
    BUY when the MACD line crosses above the signal line
    SELL (or short) when the MACD line crosses below the signal line


"""

import datetime as dt
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

stocks = ["AMZN", "GOOG", "MSFT"]
ohlcv_data = {}

for ticker in stocks:
    data = yf.download(ticker, period="1mo", interval="15m")
    data = data.dropna(how="any")
    ohlcv_data[ticker] = data


def macd(df, a=12, b=26, c=9):
    df = df.copy()
    df["ma_fast"] = df["Adj Close"].ewm(span=a, min_periods=a).mean()
    df["ma_slow"] = df["Adj Close"].ewm(span=b, min_periods=b).mean()
    df["macd"] = df["ma_fast"] - df["ma_slow"]
    df["signal"] = df["macd"].ewm(span=c, min_periods=c).mean()
    return df.loc[:, ["macd", "signal"]]

for ticker in ohlcv_data:
    print(ticker)
    ohlcv_data[ticker][["macd", "signal"]] = macd(ohlcv_data[ticker])

