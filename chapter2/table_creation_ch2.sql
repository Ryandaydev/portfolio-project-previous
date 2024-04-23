CREATE TABLE player (
        player_id INTEGER NOT NULL, 
        first_name VARCHAR NOT NULL, 
        last_name VARCHAR NOT NULL, 
        position VARCHAR NOT NULL,
        last_changed_date DATE, 
        PRIMARY KEY (player_id)
);

CREATE TABLE performance (
        performance_id INTEGER NOT NULL, 
        week_number VARCHAR NOT NULL, 
        fantasy_points FLOAT NOT NULL, 
        player_id INTEGER NOT NULL, 
        last_changed_date DATE,
        PRIMARY KEY (performance_id), 
        FOREIGN KEY(player_id) REFERENCES player (player_id)
);
CREATE TABLE league (
        league_id INTEGER NOT NULL, 
        league_name VARCHAR NOT NULL, 
        scoring_type VARCHAR NOT NULL,
        last_changed_date DATE,  
        PRIMARY KEY (league_id)
);

CREATE TABLE team (
        team_id INTEGER NOT NULL, 
        team_name VARCHAR NOT NULL, 
        league_id INTEGER NOT NULL, 
        last_changed_date DATE, 
        PRIMARY KEY (team_id), 
        FOREIGN KEY(league_id) REFERENCES league (league_id)
);

CREATE TABLE team_player (
        team_id INTEGER NOT NULL, 
        player_id INTEGER NOT NULL, 
        last_changed_date DATE, 
        PRIMARY KEY (team_id, player_id), 
        FOREIGN KEY(team_id) REFERENCES team (team_id), 
        FOREIGN KEY(player_id) REFERENCES player (player_id)
);
