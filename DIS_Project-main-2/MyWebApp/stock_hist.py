from flask import Blueprint, render_template
import yfinance as yf
from flask_login import login_required, current_user
from db_manager import db_manager

from datetime import datetime
hist  = Blueprint('hist',__name__)

def fetch_stock_history(symbol):
    ticker = yf.Ticker(symbol)
    end_date = datetime.now().strftime('%Y-%m-%d')
    hist = ticker.history(period="1mo")
    return hist

def get_closing_prices(symbol):
    hist = fetch_stock_history(symbol)
    hist = hist.to_dict()
    closing_price = list(hist['Close'].values())
    closing_price = [round(x, 2) for x in closing_price]
    closing_price = closing_price[::-1]
    return closing_price

def get_open_prices(symbol):
    hist = fetch_stock_history(symbol)
    hist = hist.to_dict()
    open_price = list(hist['Open'].values())
    open_price = [round(x, 2) for x in open_price]
    open_price = open_price[::-1]
    return open_price

def get_high_prices(symbol):
    hist = fetch_stock_history(symbol)
    hist = hist.to_dict()
    high_price = list(hist['High'].values())
    high_price = [round(x, 2) for x in high_price]
    high_price = high_price[::-1]
    return high_price
def get_date(symbol):   
    hist = fetch_stock_history(symbol)
    hist = list(hist.index.values)
    hist = [str(x) for x in hist]
    hist = [x[5:10] for x in hist]
    return hist


def get_low_prices(symbol):
    hist = fetch_stock_history(symbol)
    hist = hist.to_dict()
    low_price = list(hist['Low'].values())
    low_price = [round(x, 2) for x in low_price]
    low_price = low_price[::-1]
    return low_price

def get_volume(symbol):
    hist = fetch_stock_history(symbol)
    hist = hist.to_dict()
    volume = list(hist['Volume'].values())
    volume = [round(x, 2) for x in volume]
    volume = volume[::-1]
    return volume


def to_database(symbol): 
    cur = db_manager.get_cursor()
    open_prices = get_open_prices(symbol)
    close_prices = get_closing_prices(symbol)
    high_prices = get_high_prices(symbol)
    low_prices = get_low_prices(symbol)
    volumes = get_volume(symbol)
    dates = get_date(symbol) 
    name = yf.Ticker(symbol).info['longName']
    # Assuming the lists are all the same length and in the correct order by date
    for i in range(len(open_prices)):
        cur.execute("INSERT INTO stock_history (stock_id, open_price, close_price, high_price, low_price, volume) SELECT id, %s, %s, %s, %s, %s FROM stocks1 WHERE symbol = %s", (open_prices[i], close_prices[i], high_prices[i], low_prices[i], volumes[i], symbol))

    history = {
        
        'symbol': symbol,
        'date': dates,
        'opens': open_prices,
        'closes': close_prices,
        'highs': high_prices,
        'lows': low_prices,
        'vols': volumes,
        "name": name
    }

    db_manager.commit()
    return (history)

@hist.route("/history/<symbol>", methods = ['GET', 'POST'])
@login_required
def render_stock_history(symbol):
    stock_history = to_database(symbol)
    print("W")
    return render_template("history.html", user = current_user, stock_history = stock_history)

