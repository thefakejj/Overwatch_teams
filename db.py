from os import getenv
from flask_sqlalchemy import SQLAlchemy
from app import ow_app

#ow_app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
ow_app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("gres", "gresql", 1)

ow_db = SQLAlchemy(ow_app)