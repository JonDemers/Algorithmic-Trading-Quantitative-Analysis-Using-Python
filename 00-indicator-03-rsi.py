# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 10:03:55 2024

@author: demer

RSI: Relative Strength Index

From 0 to 100:
    - < 30 Stock is oversold: price will go UP
    - > 70 Stock is overbought: price will go DOWN

"""

import datetime as dt
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

stocks = ["AMZN", "GOOG", "MSFT"]
ohlcv_data = {}

for ticker in stocks:
    data = yf.download(ticker, period="1mo", interval="5m")
    data = data.dropna(how="any")
    ohlcv_data[ticker] = data


def rsi(df, n=14):
    df =  df.copy()
    df["change"] = df["Adj Close"] - df["Adj Close"].shift(1)
    df["gain"] = np.where(df["change"] >= 0, df["change"], 0)
    df["loss"] = np.where(df["change"] < 0, -1 * df["change"], 0)
    df["avgGain"] = df["gain"].ewm(alpha=1/n, min_periods=n).mean()
    df["avgLoss"] = df["loss"].ewm(alpha=1/n, min_periods=n).mean()
    df["rs"] = df["avgGain"]/df["avgLoss"]
    df["rsi"] = 100 - (100/(1+df["rs"]))
    return df["rsi"]

for ticker in ohlcv_data:
    df = ohlcv_data[ticker]
    df["rsi"] = rsi(df)


    