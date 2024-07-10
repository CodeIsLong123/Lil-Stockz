from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from db_manager import db_manager
from auth import auth

views = Blueprint('views',__name__)

@views.route('/home')
def home():
    news = print_news()
    winners = make_winners()
    return render_template("home.html", user = current_user, winners=winners, news=news)


@views.route('/')
def home1():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.sign_up'))
    return redirect(url_for('views.home'))


def winners():
    cur = db_manager.get_cursor()
    cur.execute("""SELECT stocks1.name, COUNT(DISTINCT favorites.user_id) as favorite_count
                    FROM stocks1 
                    LEFT JOIN favorites 
                    ON stocks1.id = favorites.stock_id
                    GROUP BY stocks1.id, stocks1.name""")
    favorite_counts = cur.fetchall()
    return favorite_counts

def make_winners():
    favorite_counts = winners()
    win_list = []   
    for favorite_count in favorite_counts:
        if favorite_count[1] > 0:
            win_list.append(favorite_count)
    return win_list[:5]

import requests

api_key="chjka21r01qh5480hn3gchjka21r01qh5480hn40"

def get_news():
    news = requests.get(f"https://finnhub.io/api/v1/news?category=general&token={api_key}")
    news = news.json()
    return news

def print_news():
    news_items = get_news()
    cur = db_manager.get_cursor()
    
    # create list of tuples
    news_list = [(i['headline'], i['summary'], i['url']) for i in news_items]

    # Use executemany to insert all rows at once
    cur.executemany("""INSERT INTO stock_news (headline, sum, url) VALUES (%s, %s, %s)""", news_list)


    db_manager.commit()

    fetch_news = cur.execute("""SELECT * FROM stock_news""")
    fetch_news = cur.fetchall()

    # Close the connection after you're done using it, not inside the loop

    return fetch_news[:5]


        
    

