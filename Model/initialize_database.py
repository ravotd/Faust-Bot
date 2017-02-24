import sqlite3

database_connection = sqlite3.connect('faust_bot.db')
cursor = database_connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS user (id INT , name TEXT AS PRIMARY KEY)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS user_stats(id INT AS PRIMARY KEY, characters INT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS last_seen (id INT AS PRIMARY KEY, last_seen INT)''')
database_connection.commit()
database_connection.close()
