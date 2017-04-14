# -*- coding: utf-8 -*-
import csv
import sqlite3

from flask import Blueprint, current_app, jsonify, request
from flask_cors import cross_origin

api = Blueprint('api', __name__)


def data_path(filename):
    data_path = current_app.config['DATA_PATH']
    return u"%s/%s" % (data_path, filename)


@api.route('/search', methods=['POST'])
@cross_origin(origins='http://localhost:8000')
def search():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    init_db(cursor)
    populate_db_table(cursor, 'products', data_path('products.csv'))
    populate_db_table(cursor, 'shops', data_path('shops.csv'))
    populate_db_table(cursor, 'tags', data_path('tags.csv'))
    populate_db_table(cursor, 'taggings', data_path('taggings.csv'))
    conn.commit()

    request_json = request.get_json()
    if not request_json or 'count' not in request_json or 'radius' not in request_json or 'position' not in request_json:
        return jsonify({'error': 'Missing data in request'})
    if type(request_json['count']) is not int:
        return jsonify({'error': 'Count must be provided as an integer'})
    if type(request_json['radius']) is not int:
        return jsonify({'error': 'Radius must be provided as an integer'})
    if 'lat' not in request_json['position'] or 'lng' not in request_json['position']:
        return jsonify({'error': 'Missing latitude or longitude in request'})
    if type(request_json['position']['lat']) is not float or type(request_json['position']['lng']) is not float:
        return jsonify({'error': 'Latitude and longitude must be provided as floating point numbers'})
    if 'tags' in request_json and type(request_json['tags']) is not list:
        return jsonify({'error': 'Tags much be provide as a list'})

    params = (request_json['count'],)
    cursor = conn.cursor()
    cursor.execute("SELECT p.title, p.popularity, s.lat, s.lng "
                   "FROM  products p JOIN shops s ON p.shop_id = s.id "
                   "LIMIT ?", params)
    products = map(construct_product_descriptor, cursor.fetchall())
    return jsonify({'products': products})


def construct_product_descriptor(row):
    product = {
        'title': row['title'],
        'popularity': row['popularity'],
        'shop': {
            'lat': row['lat'],
            'lng': row['lng']
        }
    }
    return product


def init_db(cursor):
    cursor.execute('''CREATE TABLE products (
        id TEXT,
        shop_id TEXT,
        title TEXT,
        popularity REAL,
        quantity INTEGER
        )''')
    cursor.execute('''CREATE TABLE shops (
        id TEXT,
        name TEXT,
        lat REAL,
        lng REAL
        )''')
    cursor.execute('''CREATE TABLE tags (
        id TEXT,
        tag TEXT
        )''')
    cursor.execute('''CREATE TABLE taggings (
        product_id TEXT,
        shop_id TEXT,
        tag_id TEXT
        )''')


INSERT_STATEMENTS = {
    'products': '''INSERT INTO products (id, shop_id, title, popularity, quantity) VALUES (?, ?, ?, ?, ?)''',
    'shops': '''INSERT INTO shops (id, name, lat, lng) VALUES (?, ?, ?, ?)''',
    'tags': '''INSERT INTO tags (id, tag) VALUES (?, ?)''',
    'taggings': '''INSERT INTO taggings (product_id, shop_id, tag_id) VALUES (?, ?, ?)'''
}


def unicode_csv_reader(utf8_data):
    csv_reader = csv.reader(utf8_data)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]


def populate_db_table(cursor, table, csv_path):
    reader = unicode_csv_reader(open(csv_path))
    cursor.executemany(INSERT_STATEMENTS.get(table), reader)
