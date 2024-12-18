import sqlite3
import os
import shutil

conn = sqlite3.connect('database.db')
c = conn.cursor()

def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS loginInfo
        (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL)''')

def clear_table(table):
    # empty the table but don't delete them
    c.execute("DELETE FROM " + table)

def clear_All():
    # get all the tables
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = c.fetchall()
    for table in tables:
        print("Clearing table " + table[0])
        clear_table(table[0])

    # empty the "uploads" folder
    if os.path.exists("uploads"):
        shutil.rmtree("uploads")
        os.mkdir("uploads")

clear_All()

conn.commit()
conn.close()