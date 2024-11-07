import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS loginInfo
    (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL)''')

conn.commit()
conn.close()