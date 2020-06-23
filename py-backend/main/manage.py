import os

from flask_script import Manager

from app import app_main
from constants.constants import APP_PORT, BIND_USERS
from services.config import config_service
from services.database import update_service

#placeholder import to trigger model creation, TODO: remove once User is used properly

app_main.create_app()
manager = Manager(app_main.pymdb_app)



@manager.command
def update_movie_db():
    update_service.update_db()


@manager.command
def run_dev_server():
    app_main.pymdb_app.run(port=APP_PORT)


@manager.command
def init_user_db():
    print("Initializing user database...")
    if not os.path.exists(config_service.get_user_db_path()):
        with app_main.pymdb_app.app_context():
            app_main.db.create_all(bind=BIND_USERS)
            print("User db created successfully!")
    else:
        print("User db already exists, doing nothing!")

if __name__ == '__main__':
    manager.run()
