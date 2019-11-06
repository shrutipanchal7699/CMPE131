from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
#class for Room 
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String(128))
    room_number = db.Column(db.Integer)
    max_occupants = db.Column(db.Integer)

    @classmethod
    def fetch_room_to_query(query):
        pass

#reservation Class 
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    check_in_date = db.Column(db.DateTime, nullable = False)
    check_out_date = db.Column(db.DateTime, nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    user = db.relationship('User',backref = db.backref('reservations', lazy = True))

    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable = False)
    room = db.relationship('Room',backref = db.backref('reservations', lazy = True))

    @classmethod
    def find_conflicting_reservations(cls, start_date, end_date):
        """ Return all reservations that fits the conditions:
            - Start date and end date are NOT both before the target start date
            - Start date and end date are NOT both after the target end date
        """
        reservations = cls.query.filter(
            and_(
                or_(
                    Reservation.check_in_date >= start_date,
                    Reservation.check_out_date >= start_date
                ),
                or_(
                    Reservation.check_in_date <= end_date,
                    Reservation.check_out_date <= end_date
                )
            )
        )

        return reservations


#class DeleteReservation(db.Model):
#models.User.query.delete()



