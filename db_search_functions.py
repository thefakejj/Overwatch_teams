from sqlalchemy.sql import text
from db import ow_db

def show_all_players():
    sql = text('''
        SELECT people.name, teams.name, countries.name, people.status
        FROM people, teams, people_teams_roles, countries
        WHERE people.id = people_teams_roles.person_id
        AND people_teams_roles.player_team = teams.id
        AND people.country_id = countries.id
        ''')
    result = ow_db.session.execute(sql)
    selection = result.fetchall()
    return selection

def searching_player_name(input):
    if input == '':
        selection = show_all_players()
    else:
        input = input.lower()
        sql = text('''
            SELECT people.name, teams.name, countries.name, people.status
            FROM people, teams, people_teams_roles, countries
            WHERE people.id = people_teams_roles.person_id
            AND people_teams_roles.player_team = teams.id
            AND people.country_id = countries.id
            AND LOWER(people.name) LIKE '%:input%'
        ''')
        result = ow_db.session.execute(sql, {"input":input})
        selection = result.fetchall()
    return selection


    # start of a subselect for future reference"SELECT teams.id, teams.name, people_teams_roles"