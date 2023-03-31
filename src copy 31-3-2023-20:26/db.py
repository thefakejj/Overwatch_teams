from app import ow_app
from flask_sqlalchemy import SQLAlchemy

ow_app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://"
ow_db = SQLAlchemy(ow_app)

