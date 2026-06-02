-- The job of this file is to reset all of our important database tables.
-- And add any data that is needed for the tests to run.
-- This is so that our tests, and application, are always operating from a fresh
-- database state, and that tests don't interfere with each other.

TRUNCATE play_participant CASCADE;

DROP TABLE IF EXISTS play_participant;
DROP SEQUENCE IF EXISTS play_participant_id_seq;

CREATE TABLE play_participant (
    play_id     INTEGER         NOT NULL REFERENCES play(id) ON DELETE CASCADE,
    player_id   INTEGER         NOT NULL REFERENCES player(id) ON DELETE RESTRICT,
    is_winner   BOOLEAN         NOT NULL DEFAULT FALSE,
    rating      SMALLINT        CHECK (rating BETWEEN 1 AND 10),
    PRIMARY KEY (play_id, player_id)
);

INSERT INTO play_participant (play_id, player_id, is_winner, rating)
VALUES 
    (1, 1, True, 7),
    (1, 2, False, 8),
    (1, 3, False, 5),
    (2, 2, False, 9),
    (2, 1, False, 10),
    (3, 5, False, 1),
    (3, 4, True, 9);