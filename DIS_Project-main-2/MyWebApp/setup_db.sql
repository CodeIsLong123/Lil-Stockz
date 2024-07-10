CREATE TABLE IF NOT EXISTS users (
id  SERIAL PRIMARY KEY, 
email VARCHAR(255), 
first_name VARCHAR(255), 
password VARCHAR(255));

CREATE TABLE IF NOT EXISTS stocks1 (
id SERIAL PRIMARY KEY,
symbol VARCHAR(255),
name VARCHAR(255),
price NUMERIC(10,2),
total NUMERIC(10,2),
open_price NUMERIC(10,2) CHECK (open_price >= 0),
high_price NUMERIC(10,2) CHECK (high_price >= 0),
low_price NUMERIC(10,2) CHECK (low_price >= 0),
close_price NUMERIC(10,2) CHECK (close_price >= 0),
CONSTRAINT stocks1_id_unique UNIQUE (id),
CONSTRAINT stocks1_symbol_unique UNIQUE (symbol));

CREATE TABLE IF NOT EXISTS stock_details (
id SERIAL PRIMARY KEY,
symbol VARCHAR(255) UNIQUE,
name VARCHAR(255),
stock_id INTEGER,
buisness_description1 Text,
sector VARCHAR(255),
currency VARCHAR(255),
FOREIGN KEY (stock_id) REFERENCES stocks1 (id));


CREATE TABLE IF NOT EXISTS favorites (
id SERIAL PRIMARY KEY,
user_id INTEGER,
stock_id INTEGER,
CONSTRAINT unique_user_stock UNIQUE (user_id, stock_id),
FOREIGN KEY (user_id) REFERENCES users (id),
FOREIGN KEY (stock_id) REFERENCES stocks1 (id));


CREATE TABLE IF NOT EXISTS stock_history (
stock_id INTEGER,   
name VARCHAR(255),
date VARCHAR(255),
open_price FLOAT,
high_price FLOAT,
low_price FLOAT,
close_price FLOAT,
volume BIGINT,
FOREIGN KEY (stock_id) REFERENCES stocks1 (id));

CREATE TABLE IF NOT EXISTS stock_news (
id SERIAL PRIMARY KEY,
headline VARCHAR(255),
sum Text,
url VARCHAR(255),
date VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS ratings (
id SERIAL PRIMARY KEY,
user_id INTEGER,
stock_id INTEGER,
rating Text,
FOREIGN KEY (user_id) REFERENCES users (id),
FOREIGN KEY (stock_id) REFERENCES stocks1 (id));

