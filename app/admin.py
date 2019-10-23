from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app import app, db
from app.models import User

admin = Admin(app, name='hotelApp')
admin.add_view(ModelView(User, db.session))
