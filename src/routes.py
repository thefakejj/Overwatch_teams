from app import ow_app
from db import ow_db
import db
from flask_sqlalchemy import SQLAlchemy
from flask import redirect, render_template, request
from sqlalchemy.sql import text
import add_countries


@ow_app.route("/")
def ow_index():
    lol()
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


#insert countries into table
def lol():
    countries_table_count = ow_db.session.execute(text('SELECT count(*) from countries;')).fetchone()[0]
    if countries_table_count < 1:
        add_countries.insert_countries()
    else:
        print("countries exist in the table")
    




