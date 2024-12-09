import sqlite3

connection = sqlite3.connect('products.db')
cursor = connection.cursor()

user_connection = sqlite3.connect('users.db')
user_cursor = user_connection.cursor()

def initiate_db():
    cursor.execute('''
    CREATE TABLE  IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price INTEGER
    )
    ''')
    print("Products создан")

    user_cursor.execute('''
    CREATE TABLE  IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    balance INTEGER NOT NULL
    )
    ''')
    print("Users создан")

def get_all_products():
    cursor.execute('''
    SELECT * FROM Products 
    ''')

    all_products = cursor.fetchall()

    return all_products

def is_included(username):
        user_cursor.execute("SELECT COUNT(*) FROM Users WHERE username = ?", (username,))
        return user_cursor.fetchone()[0] > 0

def add_user(username, email, age):
        user_cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                (username, email, age, 1000))

