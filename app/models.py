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

    def delete_reservation(self, res_id):
        target =  Reservation.query.get(int(res_id))
        if target and target.user_id == self.id:
            db.session.delete(target)
            db.session.commit()
            return True
        return False

    
#class for Room 
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accomodations = db.Column(db.String(128), nullable=False)
    room_type = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Float, nullable=False)
    max_occupants = db.Column(db.Integer, nullable=False)

    @classmethod
    def fetch_room_to_query(cls, query):
        """
        Expected query object:
            check_in_date (required)- date user intends to check in
            check_out_date (required) - date user intends to check out
            room_type - type of room
            num_occupants - number of occupants user intends to bring
        """
        #Construct query
        rooms = cls.query
        if query['room_type']:
            rooms = rooms.filter(Room.room_type == query['room_type'])
        if query['num_occupants']:
            rooms = rooms.filter(Room.max_occupants >= query['num_occupants'])
        #Return a list
        rooms = rooms.all()
        rooms = filter(
            lambda room: room.is_available_between(query['check_in_date'], query['check_out_date']), 
            rooms)

        return list(rooms)

    def is_available_between(self, start, end):
        """
        Given a start date and end date, 
        check if the room is wholy available between that time period
        """
        conflicting_reservations = Reservation.find_conflicting_reservations(self.id, start, end)
        # return true if no conflicting reservations exist
        return len(conflicting_reservations) == 0

#reservation Class 
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    check_in_date = db.Column(db.Date, nullable = False)
    check_out_date = db.Column(db.Date, nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    user = db.relationship('User',backref = db.backref('reservations', lazy = True))

    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable = False)
    room = db.relationship('Room',backref = db.backref('reservations', lazy = True))

    @classmethod
    def find_conflicting_reservations(cls, room_id, start_date, end_date):
        """ Return all reservations that fits the conditions:
            - Reserved for room with id room_id
            - Start date and end date are NOT both before the target start date
            - Start date and end date are NOT both after the target end date
        """
        reservations = cls.query.filter(
            Reservation.room_id == room_id,
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
        return reservations.all()

    @classmethod
    def fetch_users_reservation(cls, user_id):
        reservations = cls.query.filter(Reservation.user_id == user_id)
        return reservations
    

#class DeleteReservation(db.Model):
#models.User.query.delete()



