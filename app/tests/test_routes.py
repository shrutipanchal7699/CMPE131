from flask_testing import TestCase
from app import create_app
from app.config import TestConfig

class RouteTest(TestCase):

    def create_app(self):
        return create_app(TestConfig)

    def test_home_page(self):
        response = self.client.get('/')
        assert response.status_code == 200

    def test_auth_page(self):
        response = self.client.get('/auth')
        assert response.status_code == 200

    def test_room_list_page(self):
        response = self.client.get('/rooms')
        assert response.status_code == 200

    def test_room_detail_page(self):
        response = self.client.get('/rooms/2')
        assert response.status_code == 200
