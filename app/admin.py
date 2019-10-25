from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app import app, db
from app.models import User, Room, Reservation

admin = Admin(app, name='hotelApp')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Room, db.session))
admin.add_view(ModelView(Reservation, db.session))
