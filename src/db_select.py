from sqlalchemy.sql import text
from db import ow_db


def select_tournaments():
    result = ow_db.session.execute(text('SELECT id, name FROM tournaments'))
    selection = result.fetchall()
    return selection

def select_countries():
    result = ow_db.session.execute(text('SELECT id, name FROM countries'))
    selection = result.fetchall()
    return selection

def select_people():
    result = ow_db.session.execute(text('SELECT id, name FROM people'))
    selection = result.fetchall()
    return selection

def select_teams():
    result = ow_db.session.execute(text('SELECT id, name FROM teams'))
    selection = result.fetchall()
    return selection

def select_people_is_player():
    result = ow_db.session.execute(text('SELECT people.id, people.name FROM people, people_teams_roles WHERE people.id = people_teams_roles.person_id AND people_teams_roles.player_team IS NOT null'))
    selection = result.fetchall()
    return selection

def has_persons_in_game_roles_been_set(person_id):
    result  = ow_db.session.execute(text(f'SELECT * from in_game_roles where person_id = {person_id}'))
    selection = result.fetchall()
    if len(selection) == 0:
        return True
    else:
        return False
    
def have_persons_team_roles_been_set(person_id):
    result  = ow_db.session.execute(text(f'SELECT * from people_teams_roles where person_id = {person_id}'))
    selection = result.fetchall()
    if len(selection) == 0:
        return True
    else:
        return False