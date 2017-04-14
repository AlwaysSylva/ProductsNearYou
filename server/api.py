# -*- coding: utf-8 -*-
from math import pi, cos

from flask import Blueprint, current_app, jsonify, request, g
from flask_cors import cross_origin

TAG_QUERY = "SELECT p.title as title, p.popularity as popularity, tagshops.lat as lat, tagshops.lng as lng " \
            "FROM  products p " \
            "JOIN (" \
            "SELECT s.id, s.lat, s.lng " \
            "FROM shops s JOIN taggings JOIN tags t " \
            "ON s.id = taggings.shop_id AND taggings.tag_id = t.id " \
            "WHERE t.tag IN ({}) " \
            "AND (s.lat BETWEEN ? AND ?) AND (s.lng BETWEEN ? AND ?)" \
            ") tagshops " \
            "ON p.shop_id = tagshops.id " \
            "ORDER BY p.popularity DESC " \
            "LIMIT ?"

NO_TAG_QUERY = "SELECT p.title as title, p.popularity as popularity, s.lat as lat, s.lng as lng " \
               "FROM  products p " \
               "JOIN shops s " \
               "ON p.shop_id = s.id " \
               "WHERE (s.lat BETWEEN ? AND ?) AND (s.lng BETWEEN ? AND ?) " \
               "ORDER BY p.popularity DESC " \
               "LIMIT ?"

api = Blueprint('api', __name__)


def data_path(filename):
    data_path = current_app.config['DATA_PATH']
    return u"%s/%s" % (data_path, filename)


@api.route('/search', methods=['GET'])
@cross_origin(origins='http://localhost:8000')
def search():
    try:
        count, lat, lng, radius, tags = extract_request_args(request)
    except (TypeError, ValueError) as e:
        return jsonify_error("Invalid request arguments: " + str(e))

    # Calculate approximation of min/max for lat & lng with given radius
    r_earth = 6371000
    degrees_radius = (180 / pi) * radius / r_earth
    max_lat = lat + degrees_radius
    min_lat = lat - degrees_radius
    lng_degrees_radius = degrees_radius / cos(lat * pi / 180)
    max_lng = lng + lng_degrees_radius
    min_lng = lng - lng_degrees_radius

    params = tuple(tags) + (min_lat, max_lat, min_lng, max_lng, count)
    tag_placeholders = ', '.join('?' for tag in tags)
    cursor = g.db.cursor()
    if tags:
        cursor.execute(TAG_QUERY.format(tag_placeholders), params)
    else:
        cursor.execute(NO_TAG_QUERY, params)
    products = map(construct_product_descriptor, cursor.fetchall())
    return jsonify({'products': products})


def extract_request_args(request):
    if any(key not in request.args for key in ('count', 'radius', 'lat', 'lng')):
        raise TypeError('Required arguments - count, radius, lat, lng')
    count = request.args.get('count', type=int)
    if count is None:
        raise ValueError('count must be an int')
    radius = request.args.get('radius', type=int)
    if radius is None:
        raise ValueError('radius must be an int')
    lat = request.args.get('lat', type=float)
    if lat is None:
        raise ValueError('lat must be a float')
    lng = request.args.get('lng', type=float)
    if lng is None:
        raise ValueError('lng must be a float')
    tags = request.args.getlist('tags[]')
    return count, lat, lng, radius, tags


def jsonify_error(message):
    return jsonify({'error': message})


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
