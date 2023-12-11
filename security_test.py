from datetime import datetime, time, timezone
import os
from ib_insync import *
from pytz import timezone
import csv
ib = IB()
ib.connect('18.223.238.22',7497,clientId=1)


def close_open_orders():
    open_trades = ib.reqAllOpenOrders()
    for trade in open_trades:
        if isinstance(trade, Trade):
            order = trade.order
            print(order)
            ib.cancelOrder(order=order)

# def close_open_orders():
#     tradesss = ib.openTrades()
#     print(tradesss)
#     print("entered here")
#     open_trades = ib.reqAllOpenOrders()
#     print(open_trades)
#     for trade in open_trades:
#         if isinstance(trade, Trade):
            
#             order = trade.order
#             print(order)
#             ib.cancelOrder(order)
    
    # # print(f"Open orders are {open_js}")
    # try:
    # # Request all open orders
    #     open_trades = ib.reqAllOpenOrders()
    #     print(open_trades)
        

    #     # Iterate through open orders and cancel each one
    #     for trade in open_trades:
    #         if isinstance(trade, Trade):
    #             order = trade.contract.conId
    #             order_status = trade.orderStatus
    #             if order_status and hasattr(order_status, 'orderId'):
    #                 order_id = order_status.orderId
    #                 print(f"{order_id}")
    #             print(f"Cancelling order: {order.orderId}")
    #             ib.cancelOrder(order)
    #             print(f"Order {order.orderId} cancellation request sent.")
                
    # except Exception as e:
    #     print(f"Error: {e}")     
            

def close_open_positions():

#     positions = ib.portfolio()

#     for position in positions:
#         contract = position.contract
#         action = None
#         sqoff = None
#         # sqoff = Stock(pos.contract.symbol,"SMART",pos.contract.currency)
#         if contract.secType == 'STK':
#             if position.position > 0:
#                 action = 'SELL'
#                 sqoff = Stock(contract.symbol, contract.exchange, contract.currency)
#             elif position.position < 0:
#                 action = 'BUY'
#                 sqoff = Stock(contract.symbol, contract.exchange, contract.currency)
# # sqoff = Option(pos.contract.symbol,pos.contract.lastTradeDateOrContractMonth,pos.contract.strike,pos.contract.right,"SMART",pos.contract.multiplier,pos.contract.currency)

#         elif contract.secType == 'OPT':
#             if position.position > 0:
#                 action = 'SELL'
#                 sqoff = Option(
#                     contract.symbol,
#                     contract.lastTradeDateOrContractMonth,
#                     contract.strike,
#                     contract.right,
#                     contract.exchange,
#                     contract.multiplier,
#                     contract.currency
#                 )
#             elif position.position < 0:
#                 action = 'BUY'
#                 sqoff = Option(
#                     contract.symbol,
#                     contract.lastTradeDateOrContractMonth,
#                     contract.strike,
#                     contract.right,
#                     contract.exchange,
#                     contract.multiplier,
#                     contract.currency
#                 )

#         if action and sqoff:
#             # Qualify the contract
#             ib.qualifyContracts(sqoff)

#             # Place a market order to close the position
#             order = MarketOrder(action, abs(position.position))
#             ib.placeOrder(sqoff, order)
#             print("Positions squared off successfully")



    possy = ib.portfolio()
    print(possy)
    for pos in possy :
        contract = pos.contract
        if contract.secType == 'STK' :
            if pos.position > 0 :
                action = 'SELL'
                sqoff = Stock(pos.contract.symbol,"SMART",pos.contract.currency)
                ib.qualifyContracts(sqoff)
            elif pos.position < 0 :
                action = 'BUY'
                sqoff = Stock(pos.contract.symbol,"SMART",pos.contract.currency)
                ib.qualifyContracts(sqoff)
        elif contract.secType == 'OPT':
            if pos.position > 0 :
                action = 'SELL'
                sqoff = Option(pos.contract.symbol,pos.contract.lastTradeDateOrContractMonth,pos.contract.strike,pos.contract.right,"SMART",pos.contract.multiplier,pos.contract.currency)
                ib.qualifyContracts(sqoff)
            elif pos.position < 0 :
                action = 'BUY'
                sqoff = Option(pos.contract.symbol,pos.contract.lastTradeDateOrContractMonth,pos.contract.strike,pos.contract.right,"SMART",pos.contract.multiplier,pos.contract.currency)
                ib.qualifyContracts(sqoff)
        Order = MarketOrder(action, abs(pos.position))
        ib.placeOrder(sqoff, Order)
        

    # for pos in possy :
    #     contract = pos.contract
    #     if contract.secType == 'STK':
    #         print(f"Stock Position: {contract.symbol} - Quantity: {pos.position}")
    #     elif contract.secType == 'OPT':
    #         print(f"Option Position: {contract.symbol} - Quantity: {pos.position}")
    #     else:
    #         print(f"Unknown Position Type: {contract.secType}")
    # Stock(positions.contract.symbol,)
    # print(positions)
    # for position in positions:
    #     if position.position > 0:
    #         action = 'SELL'
    #         contract = Option(position.contract.symbol,position.contract.lastTradeDateOrContractMonth,position.contract.strike,position.contract.right,"SMART")
    #         ib.qualifyContracts(contract)
    #     elif position.position < 0:
    #         action = 'BUY'

    #         contract = Option(position.contract.symbol,position.contract.lastTradeDateOrContractMonth,position.contract.strike,position.contract.right,"SMART")
    #         ib.qualifyContracts(contract)
    #         # contract = Option(position.contract.symbol,position.contract.lastTradeDateOrContractMonth,position.contract.strike,position.contract.right,"SMART")

    #     else:
    #         continue
    #     print(contract)
    #     print(ib.openOrders())
    #     order = MarketOrder(action, abs(position.position))
    #     ib.placeOrder(contract, order)



def get_expiry_date():
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y%m%d")
    return formatted_date

def live_data(contracts):

    # Qualify contracts (you only need to do this once)
    ib.qualifyContracts(contracts)
    ib.reqMktData(contracts)

    # Set market data type
    ib.reqMarketDataType(1)

    # Wait for the market data to arrive (you can adjust the time as needed)
    ib.sleep(3)

    # Fetch the LTP for each contract
    ltps = ib.ticker(contracts).last
    print(f"{ltps} is the ltp")

    # Print LTPs


    return ltps



def get_qty(instrument,exp,stk,opt_type,route):
    print(f"{type(exp)} is of type expiry")
    contracts = Option(instrument, exp, stk, opt_type,route)
    ltp = live_data(contracts)
    print(f"Last Trade Price (LTP) for {contracts.symbol}: {ltp}")
    margins = get_margin()
    #qty = int(round(margins//ltp))
    qty = int(round(1000//ltp))
    print(f"Quantity is {qty//100}")
    return qty//100


def get_margin():
    account = ib.managedAccounts()[0]
    account_values = ib.accountValues(account)

# Check if any error message is received
    if isinstance(account_values, str) and 'error' in account_values.lower():
        print(f'Error received: {account_values}')
    else:
        # Filter the account values to find the 'NetLiquidation' value
        net_liquidation = next(
            (value for value in account_values if value.tag == 'NetLiquidation'), None
        )

        if net_liquidation:
            print(f'Net Liquidation: {net_liquidation.value}')
            print(type(net_liquidation.value))
            return float(net_liquidation.value)
        else:
            print('Net Liquidation not found')



def monitor(symbol, expiry, strike, right, exchange, qty):
    contract = Option(symbol, expiry, strike, right, exchange)

    account = ib.managedAccounts()[0]
    account_values = ib.accountValues(account)

    ib.qualifyContracts(contract)

    # Order creation
    order = MarketOrder("BUY", qty)
    order.account = account_values
    trade = ib.placeOrder(contract, order)
    ib.sleep(2)

    csv_file_path = 'trades_log.csv'

    # Get the last trade date from the file if available
    last_trade_date = None
    if os.path.isfile(csv_file_path):
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Assuming the 'Timestamp' field is the first field in the CSV
                last_trade_date = datetime.strptime(row['Timestamp'], '%Y-%m-%d %H:%M:%S')
                break

    # Check if it's a new day and truncate the file if necessary
    current_date = datetime.now().date()
    if last_trade_date is None or last_trade_date.date() != current_date:
        with open(csv_file_path, 'w', newline='') as csvfile:
            fieldnames = ['Timestamp', 'Entry Price', 'Exit Price', 'Lot Size', 'PnL', 'Instrument Name']
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csv_writer.writeheader()

    # Open the CSV file in 'a' (append) mode
    with open(csv_file_path, 'a', newline='') as csvfile:
        fieldnames = ['Timestamp', 'Entry Price', 'Exit Price', 'Lot Size', 'PnL', 'Instrument Name']
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        filled_qty = trade.filled()
        print(filled_qty)
        executed_price = trade.orderStatus.avgFillPrice
        print(f"Execution Price: {executed_price}")

        target_price = executed_price * 1.30
        stop_price = executed_price*0.85

        closing_time = time(16, 0)

        while True:
            current_time = datetime.now().astimezone(timezone('US/Eastern')).time()
            print(current_time)

            if current_time >= closing_time:
                print("Market closed")
                break

            ltp = live_data(contract)

            if ltp >= target_price:
                stop_price = ltp * 0.9
                save_stop = stop_price
                print("STOP Updated successfully")
            elif ltp <= stop_price:
                close_order = MarketOrder("SELL", filled_qty)
                close_order.account = "DU8009575"
                ib.placeOrder(contract, close_order)
                pnl = (ltp - executed_price) * filled_qty
                print(pnl)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                entry_price = executed_price
                exit_price = ltp
                lot_size = filled_qty
                instrument_name = f"{symbol} {expiry} {strike} {right}"
                csv_writer.writerow({
                    'Timestamp': timestamp,
                    'Entry Price': entry_price,
                    'Exit Price': exit_price,
                    'Lot Size': lot_size,
                    'PnL': pnl,
                    'Instrument Name': instrument_name
                })

                break


def fire(condition,close):
    exp = get_expiry_date()
    instrument = "SPY"
    stk = float(round(close))
    exchange = "SMART"
    if condition == 1 :
        opt_type = "C"
    elif condition == -1 :
        opt_type = "P"
    # close_open_orders()
    close_open_positions()
    qty = get_qty(instrument,exp,stk,opt_type,"SMART")
    print(qty)
    monitor(instrument,exp,stk,opt_type,exchange,qty)

# fire(1,455.93)
# close_open_positions()
# close_open_orders()