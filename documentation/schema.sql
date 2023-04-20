CREATE TABLE tournaments (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    code varchar(2) UNIQUE,
    name TEXT UNIQUE
);

CREATE TYPE person_status AS ENUM ('active', 'inactive', 'retired', 'deceased');

CREATE TABLE people (
    id SERIAL PRIMARY KEY,
    name TEXT,
    status person_status,
    country_id INTEGER REFERENCES countries,
    UNIQUE (name, country_id)
);
--status must be one of active/inactive/retired/deceased

CREATE TABLE in_game_roles (
    id SERIAL PRIMARY KEY,
    person_id INTEGER REFERENCES people UNIQUE ON DELETE CASCADE,
    damage BOOLEAN,
    tank BOOLEAN,
    support BOOLEAN
);

CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);
--city_id INTEGER REFERENCES cities,
--region_id INTEGER REFERENCES regions

CREATE TABLE people_teams_roles (
    id SERIAL PRIMARY KEY,
    person_id INTEGER REFERENCES people UNIQUE ON DELETE CASCADE,
    player_team INTEGER REFERENCES teams,
    coach_team INTEGER REFERENCES teams,
    manager_team INTEGER REFERENCES teams
);

CREATE TABLE tournaments_teams (
    id SERIAL PRIMARY KEY,
    tournament_id INTEGER REFERENCES tournaments ON DELETE CASCADE,
    team_id INTEGER REFERENCES teams ON DELETE CASCADE,
    UNIQUE (tournament_id, team_id)
);

/*
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT,
    tournament_id INTEGER REFERENCES tournaments ON DELETE CASCADE,
    UNIQUE (name, tournament_id)
);

CREATE TABLE groups_teams (
    id SERIAL PRIMARY KEY,
    group_id INTEGER REFERENCES groups ON DELETE CASCADE,
    team_id INTEGER REFERENCES teams,
    UNIQUE (group_id, team_id)
);

CREATE TABLE regions (
    id SERIAL PRIMARY KEY,
    name TEXT UNQIUE
);

CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name TEXT,
    country_id INTEGER REFERENCES countries
    UNIQUE (name, country_id)
);
*/