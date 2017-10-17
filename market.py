import os
import sqlite3
from market.config import *
from flask import Flask, request, \
    session, g, redirect, url_for, abort, \
    render_template, flash

app = Flask(__name__)

app.config.from_object(DebugConfig)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
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
    db = get_db()
    cursor = db.execute('Select * From goods')
    entries = cursor.fetchall()
    return render_template('example.html',entries=entries)

@app.route('/base', methods=['GET'])
def get_base():
    return render_template('base.html')

@app.route('/<int:product_id>', methods=['GET'])
def get_goods_detail(product_id):
    db = get_db()
    cursor = db.execute('Select * From goods Where id=%s' % (product_id))
    entries = cursor.fetchall()
    return render_template('example.html', entries=entries)


if __name__ == '__main__':
    app.run()

