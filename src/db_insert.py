import add_countries
from sqlalchemy.sql import text
from db import ow_db


# INSERT INTO tournaments (name) VALUES ('Overwatch League')
def insert_into_tournaments(name):
    sql = text('INSERT INTO tournaments (name) VALUES (:name)')
    ow_db.session.execute(sql, {"name":name})
    ow_db.session.commit()

def insert_into_teams(name):
    sql = text('INSERT INTO teams (name) VALUES (:name)')
    ow_db.session.execute(sql, {"name":name})
    ow_db.session.commit()

def insert_into_people(name, status, country_id):
    sql = text('INSERT INTO people (name, status, country_id) VALUES (:name, :status, :country_id)')
    ow_db.session.execute(sql, {"name":name, "status":status, "country_id":country_id})
    ow_db.session.commit()

def insert_into_people_teams_roles(person_id, player_team, coach_team, manager_team):
    #html gives everything to /people_teams_roles_send as string, None gives empty string. Here the function converts all valid id's to integers. 
    if person_id == '':
        person_id = None
    else:
        person_id = int(person_id)

    if player_team == '':
        player_team = None
    else:
        player_team = int(player_team)

    if coach_team == '':
        coach_team = None
    else:
        coach_team = int(coach_team)

    if manager_team == '':
        manager_team = None
    else:
        manager_team = int(manager_team)

    sql = text('INSERT INTO people_teams_roles (person_id, player, coach, manager) VALUES (:person_id, :player_team, :coach_team, :manager_team)')
    ow_db.session.execute(sql, {"person_id":person_id, "player_team":player_team, "coach_team":coach_team, "manager_team":manager_team})
    ow_db.session.commit()

def insert_into_in_game_roles(person_id, damage, tank, support):
    sql = text('INSERT INTO in_game_roles (person_id, damage, tank, support) VALUES (:person_id, :damage, :tank, :support)')
    ow_db.session.execute(sql, {"person_id":person_id, "damage":damage, "tank":tank, "support":support})
    ow_db.session.commit()

def insert_into_tournaments_teams(tournament_id, team_id):
    sql = text('INSERT INTO tournaments_teams (tournament_id, team_id) VALUES (:tournament_id, :team_id)')
    ow_db.session.execute(sql, {"tournament_id":tournament_id, "team_id":team_id})
    ow_db.session.commit()



#insert countries into table
def fill_countries_table():
    countries_table_count = ow_db.session.execute(text('SELECT count(*) from countries;')).fetchone()[0]
    if countries_table_count < 1:
        add_countries.insert_countries()
    else:
        print("countries exist in the table")