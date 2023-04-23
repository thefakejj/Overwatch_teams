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
    return render_template("index.html")


@ow_app.route("/register")
def register():
    return render_template("register.html")

@ow_app.route("/register",methods=["POST"])
def register_insert():
    username = request.form["username"]
    password = request.form["password"]
    if users_in_db.insert_user(username, password):
        users_in_db.insert_user(username, password)
        session["id"] = users_in_db.get_session_user_id(username)
        session["username"] = username
    else:
        return render_template("error.html", site="register.html", message="Username already exists")
    return redirect("/")

@ow_app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users_in_db.check_username_password(username, password)[0]:
        session["id"] = users_in_db.get_session_user_id(username)
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
    tournaments = db_select.select_tournaments()
    return render_template("tournaments.html", count=len(tournaments), tournaments=tournaments)

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
    user_id = users_in_db.get_session_user_id(session['username'])
    db_insert.insert_into_teams(name, user_id)
    return redirect("/teams")



# new sites

@ow_app.route("/new_people")
def new_people():
    # user id, necessary to determine which teams session user created
    user_id = users_in_db.get_session_user_id(session["username"])
    # necessary variables for the people table
    countries = db_select.select_countries()
    statuses = ['active', 'inactive', 'retired', 'deceased']

    # creating the team list
    teams = [None]
    for team in db_select.select_teams(user_id):
        teams.append(team)

    # choices for in game roles, if the person is a player
    choices = [(True, "Yes"), (False, "No")]
    return render_template("new_people.html", countries=countries, statuses=statuses, teams=teams, choices=choices)

@ow_app.route("/new_people_send", methods=["POST"])
def new_people_insert():
    person_id = db_select.select_all_people_count()+1
    user_id = users_in_db.get_session_user_id(session["username"])
    # people table
    name = str(request.form["name"])
    status = str(request.form["status"])
    country_id = int(request.form["country"])
    # checking if person already exists in database
    if db_select.has_person_been_added(name, country_id):
        message = "This person already exists in the database! You can edit a person's team roles or in game roles using the update functinalities."
        return render_template("error.html", site="new_people.html", message=message)

    # inserting information into people table
    db_insert.insert_into_people(name, status, country_id, user_id)

    # people teams roles table
    db_insert.insert_into_people_teams_roles(person_id, request.form["player_team"], request.form["coach_team"], request.form["manager_team"])
    
    # in game roles table
    db_insert.insert_into_in_game_roles(person_id, request.form["damage"], request.form["tank"], request.form["support"])
    return redirect("/new_people")


@ow_app.route("/update_people_teams_roles")
def update_people_teams_roles():
    user_id = users_in_db.get_session_user_id(session["username"])
    people = db_select.select_people(user_id)
    if people == []:
        message="This user has no people added! Add a person first."
        return render_template("error.html", site="index.html", message=message)
    teams = [None]
    for team in db_select.select_teams(user_id):
        teams.append(team)
    return render_template("update_people_teams_roles.html", people=people, teams=teams)

@ow_app.route("/update_people_teams_roles_send", methods=["POST"])
def update_person_team_role_insert():
    if request.form["person_id"] == '':
        return redirect("/")
    db_update.update_people_teams_roles(request.form["person_id"], request.form["player_team"], request.form["coach_team"], request.form["manager_team"])
    return redirect("/")


@ow_app.route("/update_in_game_roles")
def update_in_game_roles():
    user_id = users_in_db.get_session_user_id(session["username"])
    people_is_player = db_select.select_people_is_player(user_id)
    if people_is_player == []:
        message="This user has no players added! Add some players, or edit a person's team role."
        return render_template("error.html", site="index.html", message=message)
    choices = [(True, "Yes"), (False, "No")]
    return render_template("update_in_game_roles.html", people_is_player=people_is_player, choices=choices)

@ow_app.route("/update_in_game_roles_send", methods=["POST"])
def update_in_game_role_insert():
    if request.form["person_id"] == '':
        return redirect("/")
    if db_select.has_persons_in_game_roles_been_set(request.form["person_id"]):
        db_insert.insert_into_in_game_roles(request.form["person_id"], request.form["damage"], request.form["tank"], request.form["support"])
    else:
        db_update.update_in_game_roles(request.form["person_id"], request.form["damage"], request.form["tank"], request.form["support"])
    return redirect("/")


@ow_app.route("/tournaments_teams")
def tournaments_teams():
    user_id = users_in_db.get_session_user_id(session["username"])
    tournaments = db_select.select_tournaments()
    teams = db_select.select_teams(user_id)
    return render_template("tournaments_teams.html", tournaments=tournaments, teams=teams)

@ow_app.route("/tournaments_teams_send", methods=["POST"])
def tournament_teams_insert():
    db_insert.insert_into_tournaments_teams(request.form["tournament_id"], request.form["team_id"])
    return redirect("/tournaments_teams")