-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


CREATE DATABASE tournament;

-- create players table with id as serial and auto increment and storing name input
CREATE TABLE players ( player_id SERIAL PRIMARY KEY,
                       player_name TEXT);

-- create matches table with storing data of winner and loser.
-- Found a case where two players might play against each other, hence not setting winner, loser as unique key
CREATE TABLE matches (  match_id SERIAL PRIMARY KEY,
                        winner INT REFERENCES players(player_id),
                        loser INT REFERENCES players(player_id));

-- intermediate view which contains wins for each user
CREATE VIEW win_statistics AS SELECT player_id, count(winner) AS wins
     FROM players
     LEFT JOIN matches
     ON (players.player_id = matches.winner)
     GROUP BY player_id;

-- intermediate view which contains matches played for each user. Could have taken max wins if all matches for a round are reported
CREATE VIEW match_statistics AS SELECT player_id, count(winner) AS matches
    FROM players
    LEFT JOIN matches
    ON (players.player_id = matches.winner OR players.player_id = matches.loser)
    GROUP BY player_id;

-- view which contains standings based on the wins of all the players registered in tournament
CREATE VIEW player_standings AS SELECT p.player_id,p.player_name,w.wins,m.matches
    FROM players AS p,win_statistics AS w, match_statistics AS m
    WHERE p.player_id = w.player_id AND  w.player_id = m.player_id order by wins desc;