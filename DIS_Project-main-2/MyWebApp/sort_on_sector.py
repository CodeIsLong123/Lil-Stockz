from flask import Blueprint, render_template
from flask_login import login_required, current_user
from db_manager import db_manager


cat = Blueprint('cat', __name__)

def get_sector():
    cur = db_manager.get_cursor()
    cur.execute("""SELECT sector FROM stock_details GROUP BY sector ORDER BY sector;""")
    sectors = cur.fetchall()
    return [sector[0] for sector in sectors]

def get_stocks_by_sector(sector):
    cur = db_manager.get_cursor()
    cur.execute("""SELECT stocks1.name, stocks1.symbol FROM stocks1 JOIN stock_details 
                ON stocks1.symbol = stock_details.symbol WHERE stock_details.sector = %s 
                ORDER BY stocks1.name ASC;""", (sector,))
    stocks = cur.fetchall()
    
    return stocks


@cat.route('/sector', methods=['GET', 'POST'])
@login_required
def render_sector():
    sectors = get_sector()
    sector_stocks = {}
    for sector in sectors:
        stocks = get_stocks_by_sector(sector)
        sector_stocks[sector] = stocks
    return render_template('categories.html',user = current_user, sectors=sectors, sector_stocks=sector_stocks)


def sort_stocks_by_price():
    cur = db_manager.get_cursor()
    cur.execute("""SELECT  stocks1.symbol, stocks1.price FROM stocks1 JOIN stock_details 
                ON stocks1.symbol = stock_details.symbol ORDER BY stocks1.price DESC;""")
    stocks = cur.fetchall()
    return stocks
