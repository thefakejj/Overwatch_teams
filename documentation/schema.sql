CREATE TABLE tournaments (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    code varchar(2),
    name TEXT
);

CREATE TYPE person_status AS ENUM ('active', 'inactive', 'retired', 'deceased');

CREATE TABLE people (
    id SERIAL PRIMARY KEY,
    name TEXT,
    status person_status,
    country_id INTEGER REFERENCES countries
);
--status must be one of active/inactive/retired/deceased

CREATE TABLE in_game_roles (
    id SERIAL PRIMARY KEY,
    person_id INTEGER REFERENCES people,
    damage BOOLEAN,
    tank BOOLEAN,
    support BOOLEAN
);

CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name TEXT
);
--city_id INTEGER REFERENCES cities,
--region_id INTEGER REFERENCES regions

CREATE TABLE people_teams_roles (
    id SERIAL PRIMARY KEY,
    person_id INTEGER REFERENCES people,
    player INTEGER REFERENCES teams,
    coach INTEGER REFERENCES teams,
    manager INTEGER REFERENCES teams
);

CREATE TABLE tournaments_teams (
    id SERIAL PRIMARY KEY,
    tournament_id INTEGER REFERENCES tournaments,
    team_id INTEGER REFERENCES teams
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT,
    tournament_id INTEGER REFERENCES tournaments,
    team_id INTEGER REFERENCES teams
);

/*
CREATE TABLE regions (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name TEXT,
    country_id INTEGER REFERENCES countries
);
*/