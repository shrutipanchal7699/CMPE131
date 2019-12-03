import os
from flask_script import Manager

from app import app
from app.models import db

manager = Manager(app)

@manager.command
def resetdb():
    if os.path.exists("app/app.db"):
        os.remove("app/app.db")
    db.create_all()

if __name__ == "__main__":
    manager.run()