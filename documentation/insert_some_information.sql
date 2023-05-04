--insert into tournaments
INSERT INTO tournaments (name) VALUES ('Overwatch League');
INSERT INTO tournaments (name) VALUES ('Overwatch Contenders');
INSERT INTO tournaments (name) VALUES ('Pro-Am');
INSERT INTO tournaments (name) VALUES ('SuomiOW Greatest Hits');


--insert into teams

--OWL teams
INSERT INTO teams (name, user_id) VALUES ('Atlanta Reign', 1);
INSERT INTO teams (name, user_id) VALUES ('Boston Uprising', 1);
INSERT INTO teams (name, user_id) VALUES ('Chengdu Hunters', 1);
INSERT INTO teams (name, user_id) VALUES ('Dallas Fuel', 1);
INSERT INTO teams (name, user_id) VALUES ('Florida Mayhem', 1);
INSERT INTO teams (name, user_id) VALUES ('Guangzhou Charge', 1);
INSERT INTO teams (name, user_id) VALUES ('Hangzhou Spark', 1);
INSERT INTO teams (name, user_id) VALUES ('Houston Outlaws', 1);
INSERT INTO teams (name, user_id) VALUES ('London Spitfire', 1);
INSERT INTO teams (name, user_id) VALUES ('Los Angeles Gladiators', 1);
INSERT INTO teams (name, user_id) VALUES ('Los Angeles Valiant', 1);
INSERT INTO teams (name, user_id) VALUES ('New York Excelsior', 1);
INSERT INTO teams (name, user_id) VALUES ('San Francisco Shock', 1);
INSERT INTO teams (name, user_id) VALUES ('Seoul Dynasty', 1);
INSERT INTO teams (name, user_id) VALUES ('Seoul Infernal', 1);
INSERT INTO teams (name, user_id) VALUES ('Shanghai Dragons', 1);
INSERT INTO teams (name, user_id) VALUES ('Toronto Defiant', 1);
INSERT INTO teams (name, user_id) VALUES ('Vancouver Titans', 1);
INSERT INTO teams (name, user_id) VALUES ('Vegas Eternal', 1);
INSERT INTO teams (name, user_id) VALUES ('Washington Justice', 1);

--own teams XD
INSERT INTO teams (name, user_id) VALUES ('Yasun Hasut', 1);


--insert into people

--lets start with Toronto Defiant
--their players

INSERT INTO people (name, status, country_id, user_id) VALUES ('Hydron', 'active', 185, 1);
INSERT INTO people (name, status, country_id, user_id) VALUES ('s9mm', 'active', 185, 1);
INSERT INTO people (name, status, country_id, user_id) VALUES ('Speedily', 'active', 185, 1);
INSERT INTO people (name, status, country_id, user_id) VALUES ('Coluge', 'active', 185, 1);
INSERT INTO people (name, status, country_id, user_id) VALUES ('Ojee', 'active', 185, 1);
INSERT INTO people (name, status, country_id, user_id) VALUES ('UltraViolet', 'active', 185, 1);
INSERT INTO people (name, status, country_id, user_id) VALUES ('SirMajed', 'active', 150, 1);

--coaches

INSERT INTO people (name, status, country_id, user_id) VALUES ('Casores', 'active', 122, 1);
INSERT INTO people (name, status, country_id, user_id) VALUES ('NoHill', 'active', 36, 1);
INSERT INTO people (name, status, country_id, user_id) VALUES ('Wheats', 'active', 185, 1);

--manager

INSERT INTO people (name, status, country_id, user_id) VALUES ('Stella', 'active', 161, 1);


--me

INSERT INTO people (name, status, country_id, user_id) VALUES ('Yasu', 'active', 59, 1);

INSERT INTO people_teams_roles (person_id, player_team, coach_team, manager_team) 
VALUES (1, 17, NULL, NULL),
       (2, 17, NULL, NULL),
       (3, 17, NULL, NULL),
       (4, 17, NULL, NULL),
       (5, 17, NULL, NULL),
       (6, 17, NULL, NULL),
       (7, 17, NULL, NULL),
       (8, NULL, 17, NULL),
       (9, NULL, 17, NULL),
       (10, NULL, 17, NULL),
       (11, NULL, NULL, 17),
       (12, 21, NULL, 21);


INSERT INTO in_game_roles (person_id, damage, tank, support)
VALUES (1, 't', 'f', 'f'),
       (2, 't', 'f', 'f'),
       (3, 't', 'f', 'f'),
       (4, 'f', 't', 'f'),
       (5, 'f', 'f', 't'),
       (6, 'f', 'f', 't'),
       (7, 'f', 'f', 't'),
       (12, 't', 'f', 'f');
       