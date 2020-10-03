class Database:
    def __init__(self):
        pass

import sqlite3

db = sqlite3.open('db.sqlite3')

db.execute('SELECT pizda')
