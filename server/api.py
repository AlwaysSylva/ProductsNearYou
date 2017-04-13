# -*- coding: utf-8 -*-

from flask import Blueprint, current_app, jsonify
from flask_cors import cross_origin


api = Blueprint('api', __name__)


def data_path(filename):
    data_path = current_app.config['DATA_PATH']
    return u"%s/%s" % (data_path, filename)


@api.route('/search', methods=['GET'])
@cross_origin(origins='http://localhost:8000')
def search():
    return jsonify({'products': [
        {'title': 'Test Product',
         'popularity': '0.296',
         'shop': {'lat': '59.33265972650577',
                  'lng': '18.06061237898499'}
         }
    ]})
