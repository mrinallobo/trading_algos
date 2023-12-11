import yfinance as yf
import pandas as pd
import pandas_ta as ta
import time
import datetime
import pytz
from pytz import timezone
import security_test
import tests

def update_data():
    data = yf.download(tickers="SPY", period="1d", interval="1m")
    new_df = pd.DataFrame(data)
    period = 9
    ema = ta.ema(new_df["Close"], length=period)
    new_df["EMA"] = ema
    ny_timezone = pytz.timezone('America/New_York')
    today_ny = datetime.datetime.now(ny_timezone).replace(hour=9, minute=30, second=0, microsecond=0)
    new_df.index = pd.date_range(today_ny, periods=len(new_df), freq='T', tz=ny_timezone)
    return new_df

def trading_logic(df, last_trade, period):
    print(df)
    ema = ta.ema(df["Close"], length=period)
    vwap = ta.vwap(df["High"], df["Low"], df["Close"], df["Volume"])

    print("Updated EMA:", ema.iloc[-1])
    print("Updated VWAP:", vwap.iloc[-1])
    print("Updated Close:", df["Close"].iloc[-1])

    if ema.iloc[-1] < vwap.iloc[-1] and df["Close"].iloc[-1] < vwap.iloc[-1] and last_trade != "SELL" :
        # if ema.iloc[-1] - vwap.iloc[-1] <= -0.05:
        security_test.fire(-1, df["Close"].iloc[-1])
        print("SELL")
        last_trade = "SELL"
        return last_trade
    elif ema.iloc[-1] > vwap.iloc[-1] and df["Close"].iloc[-1] > vwap.iloc[-1] and last_trade != "BUY":
        # if ema.iloc[-1] - vwap.iloc[-1] <= 0.05:
        security_test.fire(1, df["Close"].iloc[-1])
        print("BUY")
        last_trade = "BUY"
        return last_trade
    else :
        return last_trade


def run_schedule(last_trade):
    print(f"{last_trade} is last trade")
    period = 9

    while True:
        current_time = datetime.datetime.now().astimezone(timezone('US/Eastern')).time()
        print(current_time)

        if current_time >= datetime.time(9, 30) and current_time <= datetime.time(16, 0):
            new_data = update_data()
            if new_data is not None:
               last_trade =  trading_logic(new_data, last_trade, period)
        else :
            print("Market closed")


        time.sleep(60)

if __name__ == "__main__":
    df = pd.DataFrame()
    period = 9
    data = yf.download(tickers="SPY", period="1d", interval="1m")
    ema = ta.ema(data["Close"], length=period)
    data["EMA"] = ema
    ny_timezone = pytz.timezone('America/New_York')
    today_ny = datetime.datetime.now(ny_timezone).replace(hour=9, minute=30, second=0, microsecond=0)
    data.index = pd.date_range(today_ny, periods=len(data), freq='T', tz=ny_timezone)
    print("Initial EMA:", ema.iloc[-1])
    df.index = pd.DatetimeIndex(df.index)
    vwap = ta.vwap(data["High"], data["Low"], data["Close"], data["Volume"])
    print("Initial VWAP:", vwap.iloc[-1])
    print("Initial Close:", data["Close"].iloc[-1])
    if ema.iloc[-1] < vwap.iloc[-1] and data["Close"].iloc[-1] < vwap.iloc[-1]:
        last_trade = "SELL"
    else :
        last_trade = "BUY"
    print(f"{last_trade} is last trade")
    file_path = 'us_holidays.csv'
    if tests.check_date_in_file(file_path,today_ny) == False :
        run_schedule(last_trade)
    else:
        print("Tough luck markets are closed")