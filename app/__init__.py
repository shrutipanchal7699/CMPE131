from flask import Flask

from app import config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(config.Config)

db = SQLAlchemy(app)

from app import routes