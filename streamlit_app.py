# streamlit_app.py

import streamlit as st
import pandas as pd
from binance.client import Client
import datetime

# Binance API（无需Key也可获取公开K线数据）
client = Client()

st.title("ETH 15分钟趋势识别系统")

# 获取ETH/USDT 15分钟K线
klines = client.get_klines(symbol='ETHUSDT', interval=Client.KLINE_INTERVAL_15MINUTE, limit=800)
df = pd.DataFrame(klines, columns=[
    "open_time", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "trades",
    "taker_base_vol", "taker_quote_vol", "ignore"
])
df["close"] = df["close"].astype(float)
df["time"] = pd.to_datetime(df["open_time"], unit='ms')

# 计算 MA40、MA200、MA750
df["MA40"] = df["close"].rolling(window=40).mean()
df["MA200"] = df["close"].rolling(window=200).mean()
df["MA750"] = df["close"].rolling(window=750).mean()

latest = df.iloc[-1]

st.metric("当前价格", f"{latest['close']:.2f}")
st.metric("MA40", f"{latest['MA40']:.2f}")
st.metric("MA200", f"{latest['MA200']:.2f}")
st.metric("MA750", f"{latest['MA750']:.2f}")
