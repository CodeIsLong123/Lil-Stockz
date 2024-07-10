from MyWebApp.prep_stocks import put_into_db
import time 
from MyWebApp.stock_info import put_info_into_db

print("Enter your database password")
if __name__ == '__main__':

    
    while True:  # Infinite loop to keep calling your functions every hour
        put_into_db()
        put_info_into_db()
        time.sleep(3600)  