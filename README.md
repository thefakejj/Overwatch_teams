# Overwatch teams application



Player database:
Admin can log in and add players the database. In the future, regular users will be able to add their own teams and manage them. The application would have a graphical user interface. The program would use an API to get small images of country flags, which would be displayed on the list of search results corresponding to the player's nationality code.

Users would be able to search Overwatch League players and teams with different kinds of filtering, such as region or what tournament they play in. The user can click on results to open a new page, with more details about the player or team. For example, if the user clicks on a player, the new page would show the player's nationality, role and teams they play for. Clicking a team shows the team's region, players and tournaments.

An API will be used to get images of country flags in the program.

FLAGS FROM https://flagpedia.net/

## THIS APP IS NOT AVAILABLE ON FLY.IO

## How to install

1. Clone the repository to your device and go to its root directory.

2. Make a file called .env and set its content to the following:
```
DATABASE_URL=<local-address-of-database>
SECRET_KEY=<secret-key>
```
You must create a unique secret key. You can do this by running the following command in the root directory:
```
python3 setup.py
```
Alternatively, you can go to the python interpreter using
```
$ python3
```
and run the commands:   
```
>>> import secrets
>>> secrets.token_hex(16)
```

3. Activate the virtual environment and install the requirements in the root directory.
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

4. Set database schema. (You'll need to have the psql database running)
```
psql < documentation/schema.sql
```

5.  Run the application using the command:
```
flask run
```

After you've created an account, you can run the command
```
psql < documentation/insert_some_information.sql
```
which will insert some information to the database as a test.
This information will be added with the user_id '1', so whatever the first user you created was will be able to use data added along this command.


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


Improvement idea to the general user experience design:
To reduce the time required to build teams using the database, people's teams, roles, in-game roles and other information could all be given in the same page where the person themselves is added. In pages where information is added to the database, the redirect could return to the same page, which would make adding large amounts of information easier. In the newly loaded page, there could be an indicator somewhere, which tells the user if the insert was successful, and what was just added to the database. Other possible changes could include a page, where people could be added into a specific team to make the process even faster. 

Database improvement ideas:
Data checking should be implemented, so that repeating data cannot be added. This would necessitate some functions to edit data, which is a functionality that is completely reasonable to add. However multiple people can have the same name, which makes this more difficult. Repeating references of the same person_id in tables such as people_teams_roles, however, should not be possible. The inclusion of tables for tournament groups may not be necessary, but this will be looked at later.

Although I've gone over many ideas for improvement in this readme, anyone leaving feedback is still welcome to mention any ideas that are already present in this file!


A rough overview of the database's tables:

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
	

