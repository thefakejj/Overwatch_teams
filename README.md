# Overwatch teams application


Player database:
Admin can log in and add players the database. In the future, regular users will be able to add their own teams and manage them. The application would have a graphical user interface. The program would use an API to get small images of country flags, which would be displayed on the list of search results corresponding to the player's nationality code.

Users would be able to search Overwatch League players and teams with different kinds of filtering, such as region or what tournament they play in. The user can click on results to open a new page, with more details about the player or team. For example, if the user clicks on a player, the new page would show the player's nationality, role and teams they play for. Clicking a team shows the team's region, players and tournaments.

An API will be used to get images of country flags in the program.


--Tournament matchmaker (possible):
--If a tournament has  multiple teams, the matchmaker could randomly create matchups.


Project status:
A local database exists and directory structure of the project has been created. Functionality regarding adding data to the database is largely sufficent. This has allowed me to test the database.

Current functionality:
- Automatically adding countries to the database upon loading the main page
- Adding a tournament to the database
- Adding a team to the database
- Adding a team to a tournament
- Adding people to the database
- Setting a person's position in a team
- Setting a player's in-game role 


Schema update:
The previous structure, where team_id would be in the groups table would not work, so team_id has been removed from the groups table and a new groups_teams table has been created.

Tables

Teams (name, city_id, --region_id) 

People (name, status: active/inactive/retired/deceased, country_id) 

People_teams_roles (people_id, player: teams_id, coach: teams_id, manager: teams_id)

In_game_roles (people_id, Damage: boolean, Tank: boolean, manager: Support) 

Tournaments (name) -> 1: overwatch league, 2 overwatch contenders

Tournaments_teams (tournament_id, teams_id)

Countries (code, name)

--Region (name) -> Europe, Korea, China

--Groups (name, tournaments_id) OWL_A, OWL_B, OWL_C, OWL_D

--Groups_teams (groups_id, teams_id)

--Cities (name, country_id)
	

