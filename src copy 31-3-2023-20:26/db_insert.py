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
    print(person_id, player_team, coach_team, manager_team)

    sql = text('INSERT INTO people (person_id, player, coach, manager) VALUES (:person_id, :player_team, :coach_team, :manager_team)')
    ow_db.session.execute(sql, {"person_id":person_id, "player_team":player_team, "coach_team":coach_team, "manager_team":manager_team})
    ow_db.session.commit()



#insert countries into table
def fill_countries_table():
    countries_table_count = ow_db.session.execute(text('SELECT count(*) from countries;')).fetchone()[0]
    if countries_table_count < 1:
        add_countries.insert_countries()
    else:
        print("countries exist in the table")