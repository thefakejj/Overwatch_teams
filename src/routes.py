from flask import redirect, render_template, request, session

from app import ow_app
import db_insert
import db_select
import db_update
import users_in_db

# sites intended to be kept (works from user experience standpoint)

@ow_app.route("/")
def index():
    db_insert.fill_countries_table()
    tournaments = db_select.select_tournaments()
    return render_template("index.html", count=len(tournaments), tournaments=tournaments) 


@ow_app.route("/register")
def register():
    return render_template("register.html")

@ow_app.route("/register",methods=["POST"])
def register_insert():
    username = request.form["username"]
    password = request.form["password"]
    print("1")
    # TODO: check username and password
    if users_in_db.insert_user(username, password):
        print("2")
        session["username"] = username
    else:
        print("3")
        return render_template("error.html", site="register.html", message="Username already exists")
    print("4")
    return redirect("/")

@ow_app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users_in_db.check_username_password(username, password):
        session["username"] = username
    else:
        return render_template("error.html", site="index.html", message="Invalid username or password")
    return redirect("/")

@ow_app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@ow_app.route("/tournaments")
def tournaments():
    return render_template("tournaments.html")

@ow_app.route("/tournaments_send", methods=["POST"])
def tournament_insert():
    name = request.form["name"]
    db_insert.insert_into_tournaments(name)
    return redirect("/tournaments")


@ow_app.route("/teams")
def teams():
    return render_template("teams.html")

@ow_app.route("/teams_send", methods=["POST"])
def team_insert():
    name = request.form["name"]
    db_insert.insert_into_teams(name)
    return redirect("/teams")









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
    return redirect("/people")


@ow_app.route("/people_teams_roles")
def people_teams_roles():
    people = db_select.select_people()
    teams = [None]
    for team in db_select.select_teams():
        teams.append(team)
    return render_template("people_teams_roles.html", people=people, teams=teams)

@ow_app.route("/people_teams_roles_send", methods=["POST"])
def person_team_role_insert():
    if db_select.have_persons_team_roles_been_set(request.form["person_id"]):
        db_insert.insert_into_people_teams_roles(request.form["person_id"], request.form["player_team"], request.form["coach_team"], request.form["manager_team"])
    else:
        db_update.update_people_teams_roles(request.form["person_id"], request.form["player_team"], request.form["coach_team"], request.form["manager_team"])
    return redirect("/people_teams_roles")


@ow_app.route("/in_game_roles")
def in_game_roles():
    people_is_player = db_select.select_people_is_player()
    choices = [(True, "Yes"), (False, "No")]
    return render_template("in_game_roles.html", people_is_player=people_is_player, choices=choices)

@ow_app.route("/in_game_roles_send", methods=["POST"])
def in_game_role_insert():
    if db_select.has_persons_in_game_roles_been_set(request.form["person_id"]):
        db_insert.insert_into_in_game_roles(request.form["person_id"], request.form["damage"], request.form["tank"], request.form["support"])
    else:
        db_update.update_in_game_roles(request.form["person_id"], request.form["damage"], request.form["tank"], request.form["support"])
    return redirect("/in_game_roles")


@ow_app.route("/tournaments_teams")
def tournaments_teams():
    tournaments = db_select.select_tournaments()
    teams = db_select.select_teams()
    return render_template("tournaments_teams.html", tournaments=tournaments, teams=teams)

@ow_app.route("/tournaments_teams_send", methods=["POST"])
def tournament_teams_insert():
    db_insert.insert_into_tournaments_teams(request.form["tournament_id"], request.form["team_id"])
    return redirect("/tournaments_teams")