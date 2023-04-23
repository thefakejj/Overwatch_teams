from flask import redirect, render_template, request, session, flash

from app import ow_app
import db_insert
import db_select
import db_update
import users_in_db
import db_search_functions
import formatting

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
    tournament_list = db_select.select_all_tournaments()
    return render_template("tournaments.html", count=len(tournament_list), tournament_list=tournament_list)

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
    # unfortunately with the routes being split into two (new_people and new_people_send), 
    # the send routes will not get access to the countries table unless the lists are created again.
    person_id = db_select.select_max_people_id()+1
    user_id = users_in_db.get_session_user_id(session["username"])

    # everything is created again to allow these when errors occur :/
    countries = db_select.select_countries()
    statuses = ['active', 'inactive', 'retired', 'deceased']
    teams = [None]
    for team in db_select.select_teams(user_id):
        teams.append(team)
    choices = [(True, "Yes"), (False, "No")]

    # people table
    name = request.form["name"]
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
            print("count is", count_of_in_game_roles)
    
    print("type:", type(request.form["player_team"]))
    print("form sisältää:", request.form["player_team"])
    

    # if the user selected a player_team and in game roles for the person, information is inserted into all three tables
    if request.form["player_team"] != '' and count_of_in_game_roles > 0:
        db_insert.insert_into_people(name, status, country_id, user_id)
        db_insert.insert_into_people_teams_roles(person_id, request.form["player_team"], request.form["coach_team"], request.form["manager_team"])
        db_insert.insert_into_in_game_roles(person_id, request.form["damage"], request.form["tank"], request.form["support"])
    
    # if the user player_team but no in game roles, information is inserted into all three tables
    elif request.form["player_team"] != ''  and count_of_in_game_roles == 0:
        db_insert.insert_into_people(name, status, country_id, user_id)
        db_insert.insert_into_people_teams_roles(person_id, request.form["player_team"], request.form["coach_team"], request.form["manager_team"])
        db_insert.insert_into_in_game_roles(person_id, request.form["damage"], request.form["tank"], request.form["support"])

    # if the user didn't select a player_team but did select in game roles, no information gets inserted and a corresponding error is displayed
    elif request.form["player_team"] == ''  and count_of_in_game_roles > 0:
        message = 'Person was not a player! If the person is not supposed to be a player, leave all in game roles as "No". Otherwise choose a team for the player.'
        return render_template("error.html", site="new_people.html", message=message, countries=countries, statuses=statuses, teams=teams, choices=choices)
    
    # if the user didnt select a player_team or an in game role, the person is added to the database with information inserted
    else:
        db_insert.insert_into_people(name, status, country_id, user_id)
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

# first attempt at a route that does both GET and POST
@ow_app.route("/search_players")
def search_players():

    # the search function doesnt work at all. however the page seems to list all players.
    # do not use the search, its broken
    user_id = users_in_db.get_session_user_id(session["username"])
    # get since its the default
    # we initialise with an empty input
    input = ''
    #if request method is POST

    current_player_list = db_search_functions.searching_player_name(input)
    print(current_player_list)


    return render_template("search_players.html", selection=current_player_list)


@ow_app.route("/search_players_send", methods=["POST"])
def search_players_send():
    user_id = users_in_db.get_session_user_id(session["username"])
    # get since its the default
    input = str(request.form["search"])

    current_player_list = db_search_functions.searching_player_name(input)


    return render_template("search_players.html", players=current_player_list)
