
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user,  login_required , logout_user, current_user
from werkzeug.security import generate_password_hash
from db_manager import db_manager
from User import User
auth = Blueprint('auth',__name__)


# Sets all the user interactions 
@auth.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        cur = db_manager.get_cursor()
        email = request.form.get('email')
        password = request.form.get('password')
        user = cur.execute("""SELECT * FROM users WHERE email = %s """, (email, ))
        user = cur.fetchone()
        if user :
                if password:
                    flash('Logged in succesfully', category = 'success')
                    login_user(User(id=user["id"], email=user['email'], first_name=user['first_name'], password=user['password']), remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect Password', category = 'error')
        else:
            flash('Email does not Exist', category = 'error' )
            
    
    return render_template("login.html", user = current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.sign_up'))


# Get and Post are HTTP mehtods that get and retrieve data 
@auth.route("/sign-up",  methods = ['GET', 'POST'])
def sign_up():    
    if request.method == 'POST':  
        cur = db_manager.get_cursor()
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = cur.execute("""SELECT * FROM users WHERE email = %s """, (email, ))
        print("user", user)
        if user:
            flash('Email Already exists', category = 'error')
            return redirect(url_for('auth.login'))
        else:
            if password1 == password2:
                password_hash = generate_password_hash(password1, method='sha256')
                cur.execute("""INSERT INTO users (email, first_name, password) VALUES (%s, %s, %s)""", (email, first_name, password_hash))
                db_manager.commit()
                cur.execute("""SELECT * FROM users WHERE email = %s """, (email, ))
                user = cur.fetchone()
                flash('Account created', category = 'success')
                login_user(User(id=user["id"], email=user['email'], first_name=user['first_name'], password=user['password']), remember=True)
                return redirect(url_for('views.home'))        
            else :
                flash('Passwords do not match', category = 'error')
                return redirect(url_for('auth.sign_up'))
    return  render_template("signup.html", user = current_user)