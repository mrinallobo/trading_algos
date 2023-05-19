import sqlite3
from config import DATABASE_PATH

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            symbol TEXT PRIMARY KEY,
            percentage_change REAL
        )
    """)

    conn.commit()
    conn.close()

def store_stock_data(stock_data):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    for stock in stock_data:
        c.execute("""
            INSERT OR REPLACE INTO stocks (symbol, percentage_change)
            VALUES (?, ?)
        """, (stock['symbol'], stock['percentage_change']))

    conn.commit()
    conn.close()

def get_stock_data():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM stocks")
    stock_data = c.fetchall()

    conn.close()

    return stock_data

if __name__ == "__main__":
    init_db()
