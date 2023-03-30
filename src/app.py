from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

ow_app = Flask(__name__)
ow_app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://"
ow_db = SQLAlchemy(ow_app)

@ow_app.route("/")
def ow_index():
    result = ow_db.session.execute(text('SELECT name FROM tournaments'))
    tournaments = result.fetchall()
    return render_template("index.html", count=len(tournaments), tournaments=tournaments) 



@ow_app.route("/tournaments")
def ow_new():
    return render_template("tournaments.html")

@ow_app.route("/tournaments_send", methods=["POST"])
def tournament_insert():
    name = request.form["name"]
    sql = text('INSERT INTO tournaments (name) VALUES (:name)')
    ow_db.session.execute(sql, {"name":name})
    ow_db.session.commit()
    return redirect("/")
# INSERT INTO tournaments (name) VALUES ('Overwatch League')