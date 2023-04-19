from app import ow_app
from os import getenv
from flask_sqlalchemy import SQLAlchemy

ow_app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
ow_db = SQLAlchemy(ow_app)