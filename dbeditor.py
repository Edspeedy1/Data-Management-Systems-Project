import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS loginInfo
        (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL)''')

def clear_tables():
    # empty the tables but don't delete them
    c.execute("DELETE FROM loginInfo")
    
clear_tables()

conn.commit()
conn.close()