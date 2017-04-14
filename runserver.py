# -*- coding: utf-8 -*-
import csv
import os
import sqlite3
from contextlib import closing

from flask import g

from server.app import create_app

app = create_app()


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def data_path(filename):
    data_path = app.config['DATA_PATH']
    return os.path.join(data_path, filename)


def init_db():
    with closing(connect_db()) as db:
        cursor = db.cursor()
        with app.open_resource(data_path('schema.sql'), mode='r') as f:
            cursor.executescript(f.read())
        populate_db_table(cursor, 'products', data_path('products.csv'))
        populate_db_table(cursor, 'shops', data_path('shops.csv'))
        populate_db_table(cursor, 'tags', data_path('tags.csv'))
        populate_db_table(cursor, 'taggings', data_path('taggings.csv'))
        db.commit()


INSERT_STATEMENTS = {
    'products': '''INSERT INTO products (id, shop_id, title, popularity, quantity) VALUES (?, ?, ?, ?, ?)''',
    'shops': '''INSERT INTO shops (id, name, lat, lng) VALUES (?, ?, ?, ?)''',
    'tags': '''INSERT INTO tags (id, tag) VALUES (?, ?)''',
    'taggings': '''INSERT INTO taggings (id, shop_id, tag_id) VALUES (?, ?, ?)'''
}


def unicode_csv_reader(utf8_data):
    csv_reader = csv.reader(utf8_data)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]


def populate_db_table(cursor, table, csv_path):
    reader = unicode_csv_reader(open(csv_path))
    cursor.executemany(INSERT_STATEMENTS.get(table), reader)


@app.before_request
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'db'):
        g.db = connect_db()


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', debug=True)
