# Read me

## To run the script

    Enter the folder mywebapp from the terminal
    Run the command: $ python/python3 app.py            // may take a moment
    Wait for the instruction to close the terminal in the command line
    Run the command: $ flask run                        
                        // follow the link in the terminal (will look similar to this http://127.0.0.1:5000)
    Use the APP!

    Potential causes for errors:
        The database is automatically created using the command $ psql < create_db.sql
        The database will not be created if the command does not work. Should this for
        whatever reason be a problem, then manually create a database called UID and design it
        in accordance to the sql-code in setup_db.sql

        If an error about a wrong database owner, or something akin to it, occurs, then open the settings.py
        file and write the name of the computer's database owner in the empty string (e.g. 'asgerrendsmark'). 

## Functionalities

### Sign up

### Sign up a new user

### Login a user

### Logout a user

### Homescreen

    Shows the top 5 most favorized stocks by all users

    news about Stocks and the stock market

### stocks

    Buttons:
    Sort stocks by:
    Search bar (Only stock symbols - Ex: AAPL)
    View performance of the last 30 days
    View the company profile description
    Add to watchlist

### Watchlist

    buttons:
    Search bar (Only stock symbols)
    Shows added stocks
    Remove stocks

## Company Profile

    Shows unique information about the company

## Sort by sector

    Shows a list of all stocks sorted by the sector they are operating in
    Click on the name and get a 30-day performance of the stock

## About

    Short description about us as a team
