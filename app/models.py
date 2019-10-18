from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.email)

    @classmethod
    def create(cls, email, password):
        pw_hash = generate_password_hash(password, method='sha256')
        new_user = cls(email=email, password_hash=pw_hash)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(int(id))
    
    #Accepts username and password, return the user if the login information is good
    @classmethod
    def check_login(cls, email, password):
        user = cls.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password_hash, password):
                return user

        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)
