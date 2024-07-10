import yfinance as yf
import time
import csv
import random
from db_manager import db_manager
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_stock_symbols_from_csv():
    with open('stocks.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader, None)
        stock_symbols = [row[0] for row in reader]
        return stock_symbols
    
def trim_list_random():
    stock_symbols = get_stock_symbols_from_csv()
    random_symbols = random.sample(stock_symbols, 100)
    return random_symbols

def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    high_price = info.get('dayHigh')
    low_price = info.get('dayLow')
    open_price = info.get('regularMarketOpen')
    close_price = info.get('previousClose')
    long_name = info.get('longName')
    twoHundredDayAverage=info.get('twoHundredDayAverage')
    return high_price, low_price, open_price, long_name, twoHundredDayAverage,close_price

def put_into_db():
    print("Starting put_into_db function...")
    stocks = trim_list_random()
    existing_symbols = set()
    def process_stock(stock):   
        try:
            high_price, low_price, open_price, long_name, twoHundredDayAverage,close_price = get_stock_info(stock)
            if stock not in existing_symbols:
                db_manager.insert_stock_without_id(stock, long_name, open_price, close_price, high_price, low_price, twoHundredDayAverage)
                db_manager.commit()
                existing_symbols.add(stock)
                print(f"{stock}, {long_name}, {open_price}, {close_price}, {high_price}, {low_price}, {twoHundredDayAverage} inserted into db")
                time.sleep(1)
        except Exception as e:
            print(f"Error inserting {stock} into db: {e}")
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_stock, stock) for stock in stocks]
        for future in as_completed(futures):
            future.result()

    print("All stocks inserted into db")