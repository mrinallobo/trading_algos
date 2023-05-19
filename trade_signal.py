from datetime import datetime, timedelta
import time
import sqlite3
from stock_data import get_top_gainer

# Function to place a short trade on a stock
def place_short_trade(stock_symbol, stop_loss, take_profit):
    # Code to place a short trade using your broker's API
    # Make sure to set your stop loss and take profit levels as specified
    # in your logic
    print(f"Short trade placed on {stock_symbol} with stop loss of {stop_loss} and take profit of {take_profit}")

# Main function to monitor top gainers and place short trades
def monitor_top_gainers():
    # Connect to SQLite database to store trade history
    conn = sqlite3.connect('trade_history.db')
    c = conn.cursor()

    # Create trade history table if it does not exist
    c.execute('''CREATE TABLE IF NOT EXISTS trade_history 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  symbol TEXT,
                  entry_price REAL,
                  exit_price REAL,
                  profit_loss REAL,
                  trade_time TEXT)''')
    conn.commit()

    while True:
        # Get the top gainer ticker symbol
        stock_symbol = get_top_gainer()
        
        # Place a short trade on the top gainer stock if it has not already been traded today
        trade_time = datetime.now().strftime('%Y-%m-%d')
        c.execute("SELECT * FROM trade_history WHERE symbol = ? AND trade_time = ?", (stock_symbol, trade_time))
        trade_history = c.fetchone()

        if not trade_history:
            place_short_trade(stock_symbol, stop_loss=0.01, take_profit=0.02)
            entry_price = print("mrinal")
            c.execute("INSERT INTO trade_history (symbol, entry_price, trade_time) VALUES (?, ?, ?)", (stock_symbol, entry_price, trade_time))
            conn.commit()

        # Wait for 24 hours before checking for new top gainers
        time.sleep(24 * 60 * 60)

    # Close the database connection
    conn.close()
