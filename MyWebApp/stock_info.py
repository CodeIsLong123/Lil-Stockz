from flask import Blueprint, render_template, request

from flask_login import login_required, current_user
from db_manager import db_manager
from yfinance import Ticker
info = Blueprint('info', __name__)

def get_stock_info(ticker):
    yf = Ticker(ticker)
    stock = yf.info
    
    currency = stock.get('currency')
    sector = stock.get('sector')
    summary = stock.get('longBusinessSummary')

    info = [currency, sector, summary]
    return info

def put_info_into_db():
    cur = db_manager.get_cursor()
    cur.execute("SELECT symbol FROM stocks1")
    stocks = cur.fetchall()
    
    for stock in stocks:
        currency, sector, summary = get_stock_info(stock[0])
        cur.execute(
            """
            INSERT INTO stock_details (symbol, currency, sector, buisness_description1)
            VALUES (%s, %s, %s, %s)
            """,
            (stock[0], currency, sector, summary)
        )
        db_manager.conn.commit()

    return stock



@info.route('/info/<name>', methods=['GET', 'POST'])
@login_required
def render_info_from_db(name):

    cur = db_manager.get_cursor()
    stock_info = cur.execute("""SELECT stock_details.symbol, currency, sector, buisness_description1 
                             from stock_details                                                                 
                             join stocks1 on stocks1.symbol=stock_details.symbol                                                                               
                             where stocks1.name= %s """, (name,))
    stock_info = cur.fetchall()
    

    if request.method == 'POST':
      
        submits = request.form.get("sub")
        if submits:
            print("check")


    return render_template("info.html", user=current_user, stock_info=stock_info,name = name)
