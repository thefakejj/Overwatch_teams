from sqlalchemy.sql import text
from db import ow_db

def select_users_count():
    result = ow_db.session.execute(text('SELECT count(*) FROM users'))
    selection = result.fetchone()
    return selection[0]

def select_tournaments():
    result = ow_db.session.execute(text("SELECT id, name FROM tournaments WHERE name NOT IN ('Overwatch League', 'Overwatch Contenders', 'Pro-Am', 'SuomiOW Greatest Hits')"))
    display = result.fetchall()
    return display

def select_all_tournaments():
    result = ow_db.session.execute(text('SELECT id, name FROM tournaments'))
    selection = result.fetchall()
    return selection

def select_countries():
    result = ow_db.session.execute(text('SELECT id, name FROM countries'))
    selection = result.fetchall()
    return selection

def select_people_all():
    result = ow_db.session.execute(text('SELECT id, name FROM people'))
    selection = result.fetchall()
    return selection

def select_people(user_id):
    # the user with user_id 1 is admin, therefore they should get access to everyone in whatever selection
    # the users table could have an admin column as well, then this function should be edited
    if user_id == 1:
        selection = select_people_all()
    else:
        result = ow_db.session.execute(text(f'SELECT id, name FROM people WHERE user_id = {user_id}'))
        selection = result.fetchall()
    return selection

def select_all_people_count():
    result = ow_db.session.execute(text('SELECT count(*) FROM people'))
    selection = result.fetchone()
    return selection[0]

def select_max_people_id():
    result = ow_db.session.execute(text('SELECT MAX(id) FROM people'))
    selection = result.fetchone()
    return selection[0]

def select_teams(user_id):
    result = ow_db.session.execute(text(f'SELECT id, name FROM teams WHERE user_id = {user_id}'))
    selection = result.fetchall()
    return selection

def select_people_is_player(user_id):
    result = ow_db.session.execute(text(f'SELECT people.id, people.name FROM people, people_teams_roles WHERE people.id = people_teams_roles.person_id AND people_teams_roles.player_team IS NOT null AND people.user_id = {user_id}'))
    selection = result.fetchall()
    return selection

def select_person_is_player(user_id):
    result = ow_db.session.execute(text(f'SELECT people.id, people.name FROM people, people_teams_roles WHERE people.id = people_teams_roles.person_id AND people_teams_roles.player_team IS NOT null AND people.user_id = {user_id}'))
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
        return False
    else:
        return True

def has_person_been_added(name, country_id):
    result = ow_db.session.execute(text(f"SELECT count(*) FROM people WHERE name = '{name}' AND country_id = '{country_id}'"))
    selection = result.fetchone()
    if int(selection[0]) > 0:
        return True
