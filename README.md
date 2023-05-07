# Overwatch teams application

Welcome to the Overwatch teams database app!




Team database:
You can register users and log into the app. Users can add people, teams, tournaments into the database, as well as add people to teams and teams to tournaments. Users can only handle information of the people or teams that they themselves have added to the database, however any user can add their team to any tournament that is not a professional tournament, such as the Overwatch League.

People can be players, managers or coaches for teams, but they can also be none of the forementioned. This information can be updated using the "Update people's roles on teams" function.

If a person is a player, they can be given in game roles or be left without them. Similarly to the previous functionality, this information can be updated using the "Update player's in-game roles" function.

Use the search players function to search players by name. Based on a player's nationality, this search displays country flags which come through an API by flagpedia.

FLAGS FROM https://flagpedia.net/

Overwatch 2 logo by Blizzard Entertainment

<br>

## THIS APP IS NOT AVAILABLE ON FLY.IO

<br>

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

