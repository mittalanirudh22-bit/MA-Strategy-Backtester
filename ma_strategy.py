import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

data=yf.download("INFY.NS",start="2024-01-01",end="2026-01-01")
print(data.head())


data.dropna(inplace=True)
data.index=pd.to_datetime(data.index)

data["Returns"]=data["Close"].pct_change()

data["MA20"]=data["Close"].rolling(20).mean()
data["MA50"]=data["Close"].rolling(50).mean()

data["Volatility"]=data["Returns"].rolling(20).std()
print(data["Volatility"])

data["Signal"]=0
data.loc[data["MA20"]>data["MA50"],"Signal"]=1
data.loc[data["MA20"]<data["MA50"],"Signal"]=-1


plt.figure(figsize=(12,6))
plt.plot(data["Close"],label="Price")
plt.plot(data["MA20"],label="MA20")
plt.plot(data["MA50"],label="MA50")
plt.legend()
plt.title("Prices vs Moving Averages")
plt.show()

data["Strategy Returns"]=data["Signal"].shift(1)*data["Returns"]

data["Cumulative Market"]=(1+data["Returns"]).cumprod()
data["Cumulative Strategy"]=(1+data["Strategy Returns"]).cumprod()

plt.figure(figsize=(12,6))
plt.plot(data["Cumulative Strategy"],label="MA Strategy")
plt.plot(data["Cumulative Market"],label="Buy and Hold")
plt.legend()
plt.show()

sharpe=(data["Strategy Returns"].mean()/data["Strategy Returns"].std())*(252**0.5)
print("Sharpe: ",sharpe)

cum=data["Cumulative Strategy"]
peak=cum.cummax()
drawdown=(cum-peak)/peak

max_drawdown=drawdown.min()
print("Max Drawdown:", max_drawdown)

total_returns=data["Cumulative Strategy"].iloc[-1]-1
print("Total Returns: ",total_returns)

market_returns=data["Cumulative Market"].iloc[-1]-1
print("Market Returns: ",market_returns)