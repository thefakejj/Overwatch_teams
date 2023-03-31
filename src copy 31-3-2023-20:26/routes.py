from app import ow_app
import db_insert
import db_select

from flask_sqlalchemy import SQLAlchemy
from flask import redirect, render_template, request
from sqlalchemy.sql import text



@ow_app.route("/")
def index():
    db_insert.fill_countries_table()
    tournaments = db_select.select_tournaments()
    return render_template("index.html", count=len(tournaments), tournaments=tournaments) 


@ow_app.route("/tournaments")
def tournaments():
    return render_template("tournaments.html")

@ow_app.route("/tournaments_send", methods=["POST"])
def tournament_insert():
    name = request.form["name"]
    db_insert.insert_into_tournaments(name)
    return redirect("/")


@ow_app.route("/teams")
def teams():
    return render_template("teams.html")

@ow_app.route("/teams_send", methods=["POST"])
def team_insert():
    name = request.form["name"]
    db_insert.insert_into_teams(name)
    return redirect("/")


@ow_app.route("/people")
def people():
    countries = db_select.select_countries()
    statuses = ['active', 'inactive', 'retired', 'deceased']
    return render_template("people.html", countries=countries, statuses=statuses)

@ow_app.route("/people_send", methods=["POST"])
def person_insert():
    name = request.form["name"]
    status = request.form["status"]
    country_id = int(request.form["country"])
    db_insert.insert_into_people(name, status, country_id)
    return redirect("/")


@ow_app.route("/people_teams_roles")
def people_teams_roles():
    people = db_select.select_people()
    teams = ['NULL']
    for team in db_select.select_teams():
        teams.append(team)
    return render_template("people_teams_roles.html", people=people, teams=teams)

@ow_app.route("/people_teams_roles_send", methods=["POST"])
def person_team_role_insert():
    #name = request.form["name"]
    #status = request.form["status"]
    #country_id = int(request.form["country"])
    db_insert.insert_into_people_teams_roles(request.form["person_id"], request.form["player_team"], request.form["coach_team"], request.form["manager_team"])
    return redirect("/")