from flask import Blueprint, render_template, request, flash, redirect, url_for

from flask_login import login_required, current_user, LoginManager
from db_manager import db_manager


faves  = Blueprint('faves',__name__)
login_manager = LoginManager()

def add_favorite(stock_id):
    db_manager.add_favorite(current_user.id, stock_id)
    

def remove_favorite(stock_id):
    db_manager.remove_favorite(current_user.id, stock_id)
    

@faves.route("/faves", methods = ['GET', 'POST'])
@login_required
def render_faves():
    favorites = db_manager.get_user_favorites(current_user.id)
    cur = db_manager.get_cursor()
    faves = cur.execute("""select stocks1.id
                        from favorites join stocks1 on 
                        stocks1.id=favorites.stock_id """)
    
    faves = cur.fetchall()
    fave = []
    for i in faves:
        fave.append(i[0])
    if "POST":

        delete = request.form.get("remove")
        if delete: 
            remove_favorite(delete)
            flash("This stock has been removed from your favorites", category = 'success')
            return redirect(url_for('faves.render_faves'))

    return render_template("favorites.html", user = current_user, favorites = favorites)