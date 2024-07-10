from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from db_manager import db_manager
from prep_stocks import put_into_db
stock = Blueprint('stock', __name__)

def render_stocks():
    
    cur = db_manager.get_cursor()
    cur.execute("""SELECT id, 
                    symbol, name, price, open_price, high_price, low_price, total
                    FROM stocks1
                    ORDER BY name ASC;""")
    
    stocks = cur.fetchall()
        
    return render_template("stock2.html", stocks=stocks, user=current_user)
@stock.route('/update-db')
def update_db():
    result = put_into_db()
    return result

@stock.route('/stocks', methods=['GET', 'POST'])
@login_required
def render_stocks_from_db():
    cur = db_manager.get_cursor()
    in_list = cur.execute("""select favorites.stock_id from favorites join stocks1 on stocks1.id=favorites.stock_id where favorites.user_id = %s""", (current_user.id,))
    in_list = cur.fetchall()
    if request.method == 'POST':
        stock_id = request.form.get("add")
        view_id = request.form.get("symbol")
        info_id = request.form.get("name")
        search_id = request.form.get("search")
        search_id = search_id.lower()
        if stock_id: 
            db_manager.add_favorite(current_user.id, stock_id)
            if in_list:
                for i in in_list:
                    if i[0] == int(stock_id):
                        flash("This stock is already in your favorites", category = 'error' )
                        return render_stocks()
            flash("This stock has been added to your favorites", category = 'success')
            return render_stocks()
        elif view_id:
            cur.execute("SELECT  * FROM stocks1 WHERE symbol = %s", (view_id,))
            stock_name = cur.fetchall()
            if stock_name:
                print("check")
                return redirect(url_for('hist.render_stock_history',  symbol=view_id))
        elif info_id:
            
            cur.execute("SELECT  name FROM stocks1 WHERE name = %s", (info_id,))
            stock_name = cur.fetchall()

            if stock_name:
              
                return redirect(url_for('info.render_info_from_db',  name = info_id))
        elif search_id:
            search_id = search_id.lower()
            cur.execute("SELECT * FROM stocks1 WHERE LOWER(symbol) LIKE %s", ('%' + search_id + '%',))
            matching_stocks = cur.fetchall()
            
            if matching_stocks:
                return redirect(url_for('hist.render_stock_history',  symbol = search_id))
            else:
                flash('Stock not found.')


    
    return render_stocks()
