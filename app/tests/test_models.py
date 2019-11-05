
from flask_testing import TestCase

from app import create_app
from app.config import TestConfig
from app.models import db, User

class ModelTest(TestCase):
    def create_app(self):
        return create_app(TestConfig)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
