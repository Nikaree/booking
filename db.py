import sqlite3
from flask import g
from app import app
DATABASE = 'database/database.db'

def get_db():
    # функция получение текущего подключения бд
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    # функция автоматического разрыва подключения
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()