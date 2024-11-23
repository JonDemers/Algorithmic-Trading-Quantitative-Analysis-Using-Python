# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 13:24:37 2024

@author: demer
"""

from dotenv import load_dotenv
import os

from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time

load_dotenv()

api_key = os.getenv("ALPHAVANTAGE_API_KEY")

print("ALPHAVANTAGE_API_KEY: ", api_key)


ts = TimeSeries(api_key, output_format="pandas")
data = ts.get_daily(symbol="MSFT", outputsize="full")[0]
data.columns = ["open", "high", "low", "close", "volume"]

all_tickers = ["AAPL", "MSFT", "CSCO", "AMZN", "GOOG", "FB"]
close_prices = pd.DataFrame()
for ticker in all_tickers:
    ts = TimeSeries(api_key, output_format="pandas")
    data = ts.get_daily(symbol=ticker, outputsize="full")[0]
    data.columns = ["open", "high", "low", "close", "volume"]
    close_prices[ticker] = data["close"]
