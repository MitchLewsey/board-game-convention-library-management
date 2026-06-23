-- The job of this file is to reset all of our important database tables.
-- And add any data that is needed for the tests to run.
-- This is so that our tests, and application, are always operating from a fresh
-- database state, and that tests don't interfere with each other.

TRUNCATE player CASCADE;

DROP TABLE IF EXISTS player;
DROP SEQUENCE IF EXISTS player_id_seq;

INSERT INTO player (alias)
VALUES
    ('ali'),
    ('bobby'),
    ('chaz'),
    ('di'),
    ('ed');
