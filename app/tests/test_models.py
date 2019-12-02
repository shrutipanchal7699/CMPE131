
import pytest
from flask_testing import TestCase
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError

from app import create_app
from app.config import TestConfig
from app.models import db, User, Room, RoomType

class ModelTest(TestCase):
    def create_app(self):
        return create_app(TestConfig)

    def setUp(self):
        db.create_all()

    def test_user_creation(self):
        user = User.create(email='asdf@asdf.com', password='asdfasdf')
        assert user.email == 'asdf@asdf.com'
        assert check_password_hash(user.password_hash, 'asdfasdf')

    def test_user_check_login(self):
        user = User.create(email='asdf@asdf.com', password='asdfasdf')
        assert user.check_login(
            email="asdf@asdf.com",
            password='asdfasdf'
        )

    def test_user_update_pw(self):
        user = User.create(email='asdf@asdf.com', password='asdfasdf')
        user.update_password(new_password='12341234', old_password='asdfasdf')
        assert check_password_hash(user.password_hash, '12341234')

    def test_user_get_by_id(self):
        user1 = User.create(email='asdf@asdf.com', password='asdfasdf')
        user2 = User.get_by_id(user1.id)
        assert user1.email == user2.email

    def test_user_unique(self):
        with pytest.raises(IntegrityError):
            user1 = User.create(email='asdf@asdf.com', password='asdfasdf')
            user2 = User.create(email='asdf@asdf.com', password='asdfasdf')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
