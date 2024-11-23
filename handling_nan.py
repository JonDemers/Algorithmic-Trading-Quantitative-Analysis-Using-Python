# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 10:03:55 2024

@author: demer
"""

import datetime as dt
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

stocks = ["AMZN", "MSFT", "META", "GOOG"]
start = dt.datetime.today()-dt.timedelta(365 * 14)
end = dt.datetime.today()
cl_price = pd.DataFrame()
ohlcv_data = {}

for ticker in stocks:
    data = yf.download(ticker, start, end)
    ohlcv_data[ticker] = data
    cl_price[ticker] = data["Adj Close"]


#cl_price = cl_price.ffill().bfill()
# OR
cl_price = cl_price.dropna(axis=0)

cl_price.mean()
cl_price.std()
cl_price.median()
cl_price.describe()
cl_price.head(10)
cl_price.tail(10)

daily_return = cl_price.pct_change()
shifted = cl_price.shift(1)
daily_return2 = cl_price / shifted - 1
daily_return2.describe()


rolling_return = daily_return.rolling(window=10).mean()

exponential_return = daily_return.ewm(com=10, min_periods=10).mean()

cl_price.plot(subplots=True, layout=(2,2), title="Price", grid=True)

daily_return.plot(subplots=True, layout=(2,2), title="Price", grid=True)

cumulative_product = (daily_return + 1).cumprod()

cumulative_product.plot(title="Cumulative Returns", grid=True)

fig, ax = plt.subplots()
plt.style.available
plt.style.use("seaborn-v0_8")
ax.set(title="Mean Daily Returns", xlabel="stocks", ylabel="Mean Return")
plt.bar(x=daily_return.columns, height=daily_return.std())
plt.bar(x=daily_return.columns, height=daily_return.mean())
