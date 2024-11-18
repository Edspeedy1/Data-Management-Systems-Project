import sqlite3

conn = sqlite3.connect('mydatabase.db')
c = conn.cursor()

def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS loginInfo
        (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL)''')

def clear_table(table):
    # empty the table but don't delete them
    c.execute("DELETE FROM " + table)

clear_table("SecurityInfo")

conn.commit()
conn.close()