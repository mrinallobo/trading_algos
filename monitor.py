from jugaad_data.nse import NSELive
import pandas as pd
from time import sleep
from stock_data import store_stock_data, get_stock_data
import requests
import json
from telegram import Bot

# Configure your Telegram bot token and channel username here
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHANNEL_USERNAME = "@yourchannelusername"
bot = Bot(token=TELEGRAM_BOT_TOKEN)

print("Starting the monitor.py script...")

stonks = pd.read_csv("https://www1.nseindia.com/content/indices/ind_nifty500list.csv")
stonk_list = list(stonks['Symbol'])

data = NSELive()

def authenticate_tt_blaze_api():
    # Replace the placeholders with your actual API credentials
    user_id = "91078209"
    password = "Alsymi@123"
    api_key = "c59f406509f024985d5113"
    secret_key = "Ephy567@Dv"
    
    # Authenticate with TT Blaze API
    url = "https://ttlogin.com/oms_authenticate"
    auth_data = {
        "userId": user_id,
        "password": password,
        "apiKey": api_key,
        "appKey": secret_key
    }
    headers = {'Content-Type': 'application/json'}
    auth_response = requests.post(url, data=json.dumps(auth_data), headers=headers)
    auth_token = auth_response.json().get("result").get("token")
    return auth_token

def subscribe_touchline_events(auth_token):
    # Subscribe to touchline events with the authentication token
    url = "https://ttapi.com/marketdata/touchline/subscribe"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }
    subscribe_response = requests.post(url, headers=headers)
    return subscribe_response

def handle_touchline_event(data):
    # Add your logic to handle touchline events and identify large market buy orders
    # Send a message to the Telegram channel when a large market buy order is detected
    bot.send_message(chat_id=TELEGRAM_CHANNEL_USERNAME, text=f"Large market buy order detected: {data}")

def runServer(stonk_list):
    print("Starting the runServer function...")
    auth_token = authenticate_tt_blaze_api()
    subscribe_touchline_events(auth_token)

    while True:
        # Fetch stock data from the NSE API and store it in the database
        stock_data = []
        for stonk in stonk_list:
            print("Fetching data for", stonk)
            try:
                q = data.stock_quote(stonk)
                pChange_raw = q['priceInfo']['pChange']
                pChange = float("{:.2f}".format(pChange_raw))
                stock_data.append({'symbol': stonk, 'percentage_change': pChange})
            except KeyError:
                print("Error fetching data for", stonk)
                pass
            sleep(0.1)

        print("Storing stock data in the database")
        store_stock_data(stock_data)

        # Print fetched stock data
        print("Fetched stock data:", stock_data)

        # Monitor stocks and execute trades
        stock_data_from_db = get_stock_data()
        for stonk, pChange in stock_data_from_db:
            if pChange > 10:  # change this number according to your logic
                # Your code to monitor order flow and execute trades

                print(stonk, "<<<",)
