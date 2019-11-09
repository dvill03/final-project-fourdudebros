DROP TABLE IF EXISTS runs CASCADE;
DROP TABLE IF EXISTS keywords CASCADE;

CREATE TABLE runs(
    event_name TEXT, 
    coverage_name TEXT, 
    score NUMERIC(3,2) NOT NULL, 
    run_name VARCHAR(50) NOT NULL, 
    user_name VARCHAR(30) NOT NULL, 
    PRIMARY KEY (event_name, coverage_name)
); 

CREATE TABLE keywords(
    event_id CHAR(6),
    event_title TEXT,
    term TEXT,
    desc_uid VARCHAR(10),
    con_uid VARCHAR(10);
    score NUMERIC,
    PRIMARY KEY (event_id, desc_uid)
);

CREATE TABLE users(
    user_id INTEGER,
    user_name VARCHAR(30),
    pass VARCHAR(80)
);
