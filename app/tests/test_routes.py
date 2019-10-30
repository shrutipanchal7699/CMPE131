from app import create_app
from app.config import TestConfig

import pytest

app = None
client = None

def setup_module(module):
    global app
    global client
    app = create_app(TestConfig)
    client = app.test_client()

def test_home_page():
    response = client.get('/')
    assert response.status_code == 200

def test_auth_page():
    response = client.get('/auth')
    assert response.status_code == 200

def test_room_list_page():
    response = client.get('/rooms')
    assert response.status_code == 200

def test_room_detail_page():
    response = client.get('/rooms/2')
    assert response.status_code == 200