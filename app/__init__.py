from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect


from app import config
from app.models import db
from app.login_manager import login_manager
from app.admin import admin
from app.routes import configure_routes

csrf = CSRFProtect()
 
def create_app(conf=config.Config):
    app = Flask(__name__)
    app.config.from_object(conf)

    db.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)
    csrf.init_app(app)
    configure_routes(app)

    return app

app = create_app()