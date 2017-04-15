class TestSearchAPI(object):
    def test_empty_request(self, get):
        assert get('/search').json == {
            'error': 'Invalid request arguments: Required arguments - count, radius, lat, lng'
        }

    def test_missing_count(self, get):
        assert get('/search?radius=500&lat=50&lng=50').json == {
            'error': 'Invalid request arguments: Required arguments - count, radius, lat, lng'
        }

    def test_missing_radius(self, get):
        assert get('/search?count=10&lat=50&lng=50').json == {
            'error': 'Invalid request arguments: Required arguments - count, radius, lat, lng'
        }

    def test_missing_lat(self, get):
        assert get('/search?count=10&radius=500&lng=50').json == {
            'error': 'Invalid request arguments: Required arguments - count, radius, lat, lng'
        }

    def test_missing_lng(self, get):
        assert get('/search?count=10&radius=500&lat=50').json == {
            'error': 'Invalid request arguments: Required arguments - count, radius, lat, lng'
        }

    def test_invalid_count(self, get):
        assert get('/search?count=ten&radius=500&lat=50&lng=50').json == {
            'error': 'Invalid request arguments: count must be an int'
        }

    def test_invalid_radius(self, get):
        assert get('/search?count=10&radius=onehundred&lat=50&lng=50').json == {
            'error': 'Invalid request arguments: radius must be an int'
        }

    def test_invalid_lat(self, get):
        assert get('/search?count=10&radius=500&lat=fifty&lng=50').json == {
            'error': 'Invalid request arguments: lat must be a float'
        }

    def test_invalid_lng(self, get):
        assert get('/search?count=10&radius=500&lat=50&lng=fifty').json == {
            'error': 'Invalid request arguments: lng must be a float'
        }

    def test_empty_response(self, get):
        assert get('/search?count=10&radius=500&lat=50&lng=50').json == {
            'products': []
        }

    def test_single_product_response(self, get):
        assert get('/search?count=1&radius=1&lat=59.33373122474713&lng=18.064412461767365').json == {
            'products': [
                {
                  "popularity": 0.997,
                  "shop": {
                    "lat": 59.33373122474713,
                    "lng": 18.064412461767365
                  },
                  "title": "Snygg kepa"
                }
            ]
        }

    def test_multiple_product_response(self, get):
        assert get('/search?count=10&radius=1&lat=59.33373122474713&lng=18.064412461767365').json == {
            'products': [
                {
                  "popularity": 0.997,
                  "shop": {
                    "lat": 59.33373122474713,
                    "lng": 18.064412461767365
                  },
                  "title": "Snygg kepa"
                },
                {
                  "popularity": 0.721,
                  "shop": {
                    "lat": 59.33373122474713,
                    "lng": 18.064412461767365
                  },
                  "title": u"ALE 40%, koko 98: Fred's World, pitk\u00e4hihainen paita"
                },
                {
                  "popularity": 0.54,
                  "shop": {
                    "lat": 59.33373122474713,
                    "lng": 18.064412461767365
                  },
                  "title": "boyfriend"
                },
                {
                  "popularity": 0.392,
                  "shop": {
                    "lat": 59.33373122474713,
                    "lng": 18.064412461767365
                  },
                  "title": "OxANT 4+ 300g"
                },
                {
                  "popularity": 0.224,
                  "shop": {
                    "lat": 59.33373122474713,
                    "lng": 18.064412461767365
                  },
                  "title": u"Kudd\u00f6verdrag Emma - handv\u00e4vd 65x65"
                },
                {
                  "popularity": 0.194,
                  "shop": {
                    "lat": 59.33373122474713,
                    "lng": 18.064412461767365
                  },
                  "title": u"M\u00f5nus Kama"
                }
            ]
        }

    def test_request_with_tags(self, get):
        assert get('/search?count=1&radius=1&lat=59.33373122474713&lng=18.064412461767365&tags[]=kids').json == {
            'products': [
                {
                  "popularity": 0.997,
                  "shop": {
                    "lat": 59.33373122474713,
                    "lng": 18.064412461767365
                  },
                  "title": "Snygg kepa"
                }
            ]
        }

    def test_request_with_tags_not_matched(self, get):
        assert get('/search?count=1&radius=1&lat=59.33373122474713&lng=18.064412461767365&tags[]=nomatch').json == {
            'products': []
        }
