from flask import Blueprint, render_template, request, redirect, url_for

from flask_login import current_user
from db_manager import db_manager

rate = Blueprint('rate', __name__)


def rate_stock():
    cur = db_manager.get_cursor()
    cur.execute("""SELECT stocks1.name, stocks1.symbol FROM stocks1 JOIN stock_details 
                ON stocks1.symbol = stock_details.symbol ORDER BY stocks1.name ASC;""")
    stocks = cur.fetchall()
    return stocks


def fetch_posts():
    pass

def post_ratings():
    pass
    

    
    
@rate.route('/rate', methods=['GET', 'POST'])
def forum ():
    if request.method == 'POST':
        submit = request.form.get("submit")
        if submit:
            return redirect(url_for('rate.render_rate'))
    return render_template("rate.html", user = current_user)

