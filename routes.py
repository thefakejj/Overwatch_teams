from flask import redirect, render_template, request, session, flash

from app import ow_app
import db_insert
import db_select
import db_update
import users_in_db
import db_search_functions
from formatting import format_fully, username_invalid_characters, people_name_description, tournaments_name_description, teams_name_description

import secrets

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

    if len(username) < 3:
        message = "Username should be at least 3 characters long"
    
    elif len(username) >= 36:
        message = "Username shouldn't be more than 36 characters long"
    
    elif username_invalid_characters(username):
        message = "Username has invalid characters"
    
    elif users_in_db.user_exists(username):
        message = "Username already exists"

    elif len(password) < 8:
        message = "Password should be at least 8 characters long"

    elif len(password) > 256:
        message = "Password too long"

    else:
        users_in_db.insert_user(username, password)
        session["id"] = users_in_db.get_session_user_id(username)
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")

    return render_template("error.html", site="register.html", message=message)

@ow_app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users_in_db.check_username_password(username, password):
        session["id"] = users_in_db.get_session_user_id(username)
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
    else:
        return render_template("error.html", site="index.html", message="Invalid username or password")
    return redirect("/")

@ow_app.route("/logout")
def logout():
    del session["username"]
    del session["id"]
    del session["csrf_token"]
    return redirect("/")


@ow_app.route("/tournaments")
def tournaments():
    tournament_list = db_select.select_all_tournaments()
    return render_template("tournaments.html", count=len(tournament_list), tournament_list=tournament_list)

@ow_app.route("/tournaments_send", methods=["POST"])
def tournament_insert():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
        
    name = format_fully(request.form["name"])
    if tournaments_name_description(name) != "okay":
        tournament_list = db_select.select_all_tournaments()
        message = tournaments_name_description(name)
        return render_template("error.html", site="tournaments.html", message=message, count=len(tournament_list), tournament_list=tournament_list)
    db_insert.insert_into_tournaments(name)
    return redirect("/tournaments")


@ow_app.route("/teams")
def teams():
    return render_template("teams.html")

@ow_app.route("/teams_send", methods=["POST"])
def team_insert():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    name = format_fully(request.form["name"])
    if teams_name_description(name) != "okay":
        message = teams_name_description(name)
        return render_template("error.html", site="teams.html", message=message)
    
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
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    # unfortunately with the routes being split into two (new_people and new_people_send), 
    # the send routes will not get access to the countries table unless the lists are created again.
    user_id = users_in_db.get_session_user_id(session["username"])

    # everything is created again to allow these when errors occur :/
    countries = db_select.select_countries()
    statuses = ['active', 'inactive', 'retired', 'deceased']
    teams = [None]
    for team in db_select.select_teams(user_id):
        teams.append(team)
    choices = [(True, "Yes"), (False, "No")]

    # people table
    name = format_fully(request.form["name"])
    if people_name_description(name) != "okay":
        message = people_name_description(name)
        return render_template("error.html", site="new_people.html", message=message, countries=countries, statuses=statuses, teams=teams, choices=choices)

    status = request.form["status"]
    country_id = int(request.form["country"])
    # checking if person already exists in database
    if db_select.has_person_been_added(name):
        message = "This person already exists in the database! You can edit a person's team roles or in game roles using the update functinalities."
        return render_template("error.html", site="new_people.html", message=message, countries=countries, statuses=statuses, teams=teams, choices=choices)

    # checking if at least one in game role was selected
    count_of_in_game_roles = 0
    for role in [request.form["damage"], request.form["tank"], request.form["support"]]:
        if role == 'True':
            count_of_in_game_roles += 1

    # if the user selected a player_team and in game roles for the person, information is inserted into all three tables
    if request.form["player_team"] != '' and count_of_in_game_roles > 0:
        db_insert.insert_into_people(name, status, country_id, user_id)
        person_id = db_select.select_max_people_id()
        db_insert.insert_into_people_teams_roles(person_id, request.form["player_team"], request.form["coach_team"], request.form["manager_team"])
        db_insert.insert_into_in_game_roles(person_id, request.form["damage"], request.form["tank"], request.form["support"])
    
    # if the user player_team but no in game roles, information is inserted into all three tables
    elif request.form["player_team"] != ''  and count_of_in_game_roles == 0:
        db_insert.insert_into_people(name, status, country_id, user_id)
        person_id = db_select.select_max_people_id()
        db_insert.insert_into_people_teams_roles(person_id, request.form["player_team"], request.form["coach_team"], request.form["manager_team"])
        db_insert.insert_into_in_game_roles(person_id, request.form["damage"], request.form["tank"], request.form["support"])

    # if the user didn't select a player_team but did select in game roles, no information gets inserted and a corresponding error is displayed
    elif request.form["player_team"] == ''  and count_of_in_game_roles > 0:
        message = 'Person was not a player! If the person is not supposed to be a player, leave all in game roles as "No". Otherwise choose a team for the player.'
        return render_template("error.html", site="new_people.html", message=message, countries=countries, statuses=statuses, teams=teams, choices=choices)
    
    # if the user didnt select a player_team or an in game role, the person is added to the database with information inserted
    else:
        db_insert.insert_into_people(name, status, country_id, user_id)
        person_id = db_select.select_max_people_id()
        db_insert.insert_into_people_teams_roles(person_id, request.form["player_team"], request.form["coach_team"], request.form["manager_team"])
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
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if request.form["person_id"] != '':
        if db_select.have_persons_team_roles_been_set(request.form["person_id"]):
            db_update.update_people_teams_roles(request.form["person_id"], request.form["player_team"], request.form["coach_team"], request.form["manager_team"])
        else:
            db_insert.insert_into_people_teams_roles(request.form["person_id"], request.form["player_team"], request.form["coach_team"], request.form["manager_team"])
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
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if request.form["person_id"] != '':
        if db_select.has_persons_in_game_roles_been_set(request.form["person_id"]):
            db_insert.insert_into_in_game_roles(request.form["person_id"], request.form["damage"], request.form["tank"], request.form["support"])
        else:
            db_update.update_in_game_roles(request.form["person_id"], request.form["damage"], request.form["tank"], request.form["support"])
    return redirect("/")


@ow_app.route("/tournaments_teams")
def tournaments_teams():
    user_id = users_in_db.get_session_user_id(session["username"])
    if user_id == 1:
        tournaments = db_select.select_all_tournaments()
    else:
        tournaments = db_select.select_tournaments()
    teams = db_select.select_teams(user_id)
    return render_template("tournaments_teams.html", tournaments=tournaments, teams=teams)

@ow_app.route("/tournaments_teams_send", methods=["POST"])
def tournament_teams_insert():
    db_insert.insert_into_tournaments_teams(request.form["tournament_id"], request.form["team_id"])
    return redirect("/tournaments_teams")




# sites for "search filtering". essentially these make it possible to search for teams, players, tournaments or whatever else

@ow_app.route("/search_players")
def search_players():
    # get since its the default
    # we initialise with an empty input
    input = ''

    current_player_list = db_search_functions.searching_player_name(input)


    return render_template("search_players.html", selection=current_player_list, input=input)


@ow_app.route("/search_players_send", methods=["POST"])
def search_players_send():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    input = format_fully((request.form["search"]))

    current_player_list = db_search_functions.searching_player_name(input)


    return render_template("search_players.html", selection=current_player_list, input=input)
