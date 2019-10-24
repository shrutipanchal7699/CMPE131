#Hotel Callisto

To update db:

 - delete app.db if its eists
 - in terminal: $flask shell
              >>>from app import db
              >>>db.create_all()
              >>>exit()
