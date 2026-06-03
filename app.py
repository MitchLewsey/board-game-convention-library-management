import os
from flask import Flask
from dotenv import load_dotenv
from lib.db import db

load_dotenv()


def create_app(test=False):
    app = Flask(__name__)

    if test:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("TEST_DATABASE_URL")
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    import lib.board_game

    return app