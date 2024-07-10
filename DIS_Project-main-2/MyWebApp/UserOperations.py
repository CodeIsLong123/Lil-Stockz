from User import User
from stock_class import Stock
from werkzeug.security import generate_password_hash, check_password_hash
from db_manager import db_manager


class UserOperations:

    def get_user_by_id(id):
        cursor = db_manager.get_cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        row = cursor.fetchone()
        if row:
             return User(id=row["id"], email=row['email'], password=row['password'], first_name=row['first_name'])
    
    @staticmethod
    def get_stock_by_id(stock_id):
        cursor = db_manager.get_cursor()
        cursor.execute("SELECT * FROM stocks1 WHERE id = %s", (stock_id,))
        row = cursor.fetchone()
        if row:
            return Stock(id=row[0], symbol=row[1], name=row[2], shares=row[3], price=row[4], total=row[5])
    @staticmethod
    def get_user_by_email(email):
        cursor = db_manager.get_cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s ", (email, ))
        row = cursor.fetchone()
        if row:
            
            return User(id=row["id"], email=row['email'], first_name=row['first_name'], password=row['password'])
        
    @staticmethod
    def add_user(email, first_name, password):
        cursor = db_manager.get_cursor()
        cursor.execute("INSERT INTO users (email, first_name, password) VALUES (%s, %s, %s)", (email, first_name, generate_password_hash(password, method='sha256')))
        cursor.fetchone()
        db_manager.commit()
        
    
    @staticmethod    
    def check_password(user, password):
        return check_password_hash(user.password, password)
    
        
    @staticmethod
    def verify_password(hashed_password, password):
        return check_password_hash(hashed_password, password)
    
    
    @staticmethod
    def get_stock(id):
        cursor = db_manager.get_cursor()
        cursor.execute("""SELECT * FROM stocks1""")
        stocks = cursor.fetchall()
        if stocks:
            return Stock(id=stocks["id"], symbol=stocks["symbol"], name=stocks["name"], shares=stocks["shares"], price=stocks["price"], total=stocks["total"])
    

    def get_stock_by_symbol(symbol):
        cursor = db_manager.get_cursor()
        cursor.execute("SELECT * FROM stocks1 WHERE symbol = %s", (symbol,))
        stocks = cursor.fetchone()
        if stocks: 
            return Stock(id=stocks["id"], symbol=stocks["symbol"], name=stocks["name"], shares=stocks["shares"], price=stocks["price"], total=stocks["total"])
    
    @staticmethod
    def get_stock_by_all():
        cursor = db_manager.get_cursor()
        cursor.execute("SELECT * FROM stocks1")
        rows = cursor.fetchall()
        stocks = []
        if rows: 
            for row in rows:
                stocks.append(Stock(id=row[0], symbol=row[1], name=row[2], shares=row[3], price=row[4], total=row[5]))
        return stocks
    
