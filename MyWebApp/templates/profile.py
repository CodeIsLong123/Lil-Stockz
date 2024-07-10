# from flask import Blueprint, render_template, request, flash, redirect, url_for
# from MyWebApp.UserOperations import UserOperations
# from flask_login import login_user,  login_required , logout_user, current_user
# from db_manager import db_manager
# from stocks import render_stocks


# ################################################################################
# #                        This Does not work yet                                #
# ################################################################################
# profile = Blueprint('profile', __name__)
# def get_user(): 
#     cur = db_manager.get_cursor()
#     cur.execute("SELECT * FROM users WHERE id = %s", (current_user.id,))
#     user = cur.fetchone()
#     return user

# @profile.route('/profile', methods=['GET', 'POST'])
# @login_required
# def show_profile():
#     user = get_user()
#     stock = render_stocks()    
#     return render_template("profile.html", user=current_user.id, stocks=stock)