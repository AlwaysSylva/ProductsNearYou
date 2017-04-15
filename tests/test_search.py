class TestSearchAPI(object):

    def test_empty_request(self, get):
        response = get('/search')
        assert response.json == {'error': 'Invalid request arguments: Required arguments - count, radius, lat, lng'}
