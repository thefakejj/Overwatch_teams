from sqlalchemy.sql import text
from db import ow_db
import db_service_commands

def update_in_game_roles(person_id, damage, tank, support):
    sql = text('UPDATE in_game_roles SET damage = :damage, tank = :tank, support = :support WHERE person_id = :person_id')
    ow_db.session.execute(sql, {"person_id":person_id, "damage":damage, "tank":tank, "support":support})
    ow_db.session.commit()

def update_people_teams_roles(person_id, player_team, coach_team, manager_team):
    person_id, player_team, coach_team, manager_team = db_service_commands.null_fix(person_id, player_team, coach_team, manager_team)
    sql = text('UPDATE people_teams_roles SET player_team = :player_team, coach_team = :coach_team, manager_team = :manager_team WHERE person_id = :person_id')
    ow_db.session.execute(sql, {"person_id":person_id, "player_team":player_team, "coach_team":coach_team, "manager_team":manager_team})
    ow_db.session.commit()