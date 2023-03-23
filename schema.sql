CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name TEXT,
);
--add city_id INTEGER REFERENCES cities
--add region_id INTEGER REFERENCES regions

CREATE TABLE people (
    id SERIAL PRIMARY KEY,
    name TEXT,
    status TEXT,
    country_id INTEGER REFERENCES countries
);
--status must be one of active/inactive/retired/deceased

CREATE TABLE people_teams_roles (
    id SERIAL PRIMARY KEY,
    person_id INTEGER REFERENCES people,
    player INTEGER REFERENCES teams,
    coach INTEGER REFERENCES teams,
    manager INTEGER REFERENCES teams
);

CREATE TABLE in_game_roles (
    id SERIAL PRIMARY KEY,
    person_id INTEGER REFERENCES people,
    damage BOOLEAN,
    tank BOOLEAN,
    support BOOLEAN
);

CREATE TABLE tournaments (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE tournaments_teams (
    id SERIAL PRIMARY KEY,
    tournament_id REFERENCES tournaments,
    team_id REFERENCES teams
);

CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    code varchar(2),
    name TEXT
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT,
    tournament_id REFERENCES tournaments,
    team_id REFERENCES teams
);

/*
CREATE TABLE regions (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name TEXT,
    country_id REFERENCES countries
);
*/