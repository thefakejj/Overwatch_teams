from sqlalchemy.sql import text
import add_countries
import db_service_commands
from db import ow_db


# INSERT INTO tournaments (name) VALUES ('Overwatch League')
def insert_into_tournaments(name):
    sql = text('INSERT INTO tournaments (name) VALUES (:name)')
    ow_db.session.execute(sql, {"name":name})
    ow_db.session.commit()

def insert_into_teams(name, user_id):
    sql = text(f'INSERT INTO teams (name, user_id) VALUES (:name, :user_id)')
    ow_db.session.execute(sql, {"name":name, "user_id":user_id})
    ow_db.session.commit()

def insert_into_people(name, status, country_id, user_id):
    sql = text('INSERT INTO people (name, status, country_id, user_id) VALUES (:name, :status, :country_id, :user_id)')
    ow_db.session.execute(sql, {"name":name, "status":status, "country_id":country_id, "user_id":user_id})
    ow_db.session.commit()

def insert_into_people_teams_roles(person_id, player_team, coach_team, manager_team):
    person_id, player_team, coach_team, manager_team = db_service_commands.null_fix(person_id, player_team, coach_team, manager_team)

    sql = text('INSERT INTO people_teams_roles (person_id, player_team, coach_team, manager_team) VALUES (:person_id, :player_team, :coach_team, :manager_team)')
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



# #insert countries into table
def fill_countries_table():
    countries_table_count = ow_db.session.execute(text('SELECT count(*) from countries;')).fetchone()[0]
    if countries_table_count < 1:
        add_countries.insert_countries(ow_db)
    else:
        print("countries exist in the table")