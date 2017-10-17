"""
Simplest example of the market-site on the sqlite database
see shema in schema.sql
"""

import sqlite3

from flask import Flask, g, render_template

from market.config import *

app = Flask(__name__)

app.config.from_object(DebugConfig)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection
    if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def exec_sql(sql):
    db = get_db()
    cursor = db.execute(sql)
    return cursor.fetchall()

@app.teardown_appcontext
def close_db(error):
    """Closes the database
    again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.route('/', methods=['GET'])
def get_goods_list():
    sql='Select * From goods Join images on goods.id = images.goods_id'
    entries = exec_sql(sql)
    return render_template('goods_list.html',entries=entries)

@app.route('/<int:product_id>', methods=['GET'])
def get_goods_detail(product_id):
    sql='Select * From goods Join images on goods.id = images.goods_id Where goods.id=%s' % (product_id)
    entries = exec_sql(sql)
    return render_template('goods_detail.html', entries=entries)


if __name__ == '__main__':
    app.run()
