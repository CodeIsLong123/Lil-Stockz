import psycopg2
import psycopg2.extras
from settings import user, password, host, db_name
import os
class DatabaseManager: 
    def __init__(self, db_name, user, password, host):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
   
        os.system("psql < create_db.sql")
        self.conn = psycopg2.connect(
            database=self.db_name,
            user = self.user,
            password = self.password,
            host = self.host,
            
        )
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)        


    def setup_database(self):
        os.system("psql -d UID < setup_db.sql")
    def get_cursor(self):
        return self.cur
    def commit(self):
         self.conn.commit()
    def close(self):
        pass
    def open_connection(self):
        return self.conn
    def close_connection(self):
        self.conn.close()

    def insert_stock(self, symbol, name, open, current_price, total):
        self.cur.execute("""
            INSERT INTO stocks1 (symbol, name, shares, price, total)
            VALUES (%s, %s, %s, %s, %s)
            
                         """, (symbol, name, open, current_price, total))
        self.conn.commit()  

    def get_stock(self):
        self.cur.execute("SELECT * FROM stocks1")    
        stocks = self.cur.fetchall()
        print (stocks)
        return stocks
    
    def delete_stock(self):
        self.cur.execute("DELETE FROM stocks1")
        self.conn.commit()
    
    def add_favorite(self, user_id, stock_id):
        self.cur.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM favorites WHERE user_id = %s AND stock_id = %s
            ) THEN
                INSERT INTO favorites (user_id, stock_id) VALUES (%s, %s);
            END IF;
        END $$;
        """, (user_id, stock_id, user_id, stock_id))
        self.conn.commit()
   
    def remove_favorite(self, user_id, stock_id):
        self.cur.execute("""
        DELETE FROM favorites WHERE user_id = %s AND stock_id = %s
    """, (user_id, stock_id))
        self.conn.commit()  
        
    def get_user_favorites(self, user_id):
        self.cur.execute("""
        SELECT s.*
        FROM favorites f
        JOIN stocks1 s ON f.stock_id = s.id
        WHERE f.user_id = %s
    """, (user_id,))
        return self.cur.fetchall()
    
    def insert_stock_without_id(self,symbol, name, open_price, current_price, high_price, close_price, low_price):

        query = """
            INSERT INTO stocks1 (symbol, name, open_price, price, high_price, close_price, low_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (symbol, name, open_price, current_price, high_price, close_price, low_price)
        self.cur.execute(query, values)

    
    
    def get_stock_history(self, stock_id):
        self.cur.execute("""
        SELECT *
        FROM stock_history
        WHERE stock_id = %s
    """, (stock_id,))
        return self.cur.fetchall()
    
    def get_ticker_symbols(self):
        self.cur.execute("SELECT symbol FROM stocks1")
        symbols = self.cur.fetchone()
        return symbols
    
    
    def update_stock_details(self, symbol, currency, sector, buisness_description1):
        self.cur.execute(
        """
        UPDATE stock_details
        SET symbol = %s, currency = %s, sector = %s, buisness_description1 = %s
        """,
        (symbol, currency, sector, buisness_description1)
    )
        self.conn.commit()
            
    def insert_stock_history(self, open_price, high_price, low_price, close_price, volume):
        self.cur.execute("""
        INSERT INTO stock_history (stock_id, name, date, open_price, high_price, low_price, close_price, volume)
        SELECT %s, %s, %s, %s, %s, %s, %s, %s
        WHERE NOT EXISTS (
            SELECT 1 FROM stock_history WHERE stock_id = %s AND date = %s
        )
    """, ( open_price, high_price, low_price, close_price, volume))
        self.conn.commit()
    
db_manager = DatabaseManager(
        db_name = db_name,
        user = user,
        password = password,
        host = host
    )

DatabaseManager.setup_database(db_manager)