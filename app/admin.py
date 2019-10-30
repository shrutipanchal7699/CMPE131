from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app.models import db, User, Room, Reservation

admin = Admin(name='hotelApp')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Room, db.session))
admin.add_view(ModelView(Reservation, db.session))
