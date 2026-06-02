-- The job of this file is to reset all of our important database tables.
-- And add any data that is needed for the tests to run.
-- This is so that our tests, and application, are always operating from a fresh
-- database state, and that tests don't interfere with each other.

TRUNCATE play CASCADE;

DROP TABLE IF EXISTS play;
DROP SEQUENCE IF EXISTS play_id_seq;

CREATE TABLE play (
    id                SERIAL      PRIMARY KEY,
    board_game_id     INTEGER     NOT NULL REFERENCES board_game(id) ON DELETE RESTRICT,
    start_time        TIMESTAMP   NOT NULL DEFAULT NOW(),
    end_time          TIMESTAMP,
    duration_minutes  SMALLINT     GENERATED ALWAYS AS (
                                    EXTRACT(EPOCH FROM (end_time - start_time)) / 60
                                  ) STORED
);

INSERT INTO play (board_game_id, start_time, end_time)
VALUES
    (1, '2026-05-15 18:30:00', '2026-05-15 19:30:00'),
    (2, '2026-06-15 12:02:42', '2026-05-15 12:27:49'),
    (3, '2026-06-15 12:02:42', '2026-05-15 12:27:49'),
    (4, '2026-05-22 18:00:00', '2026-05-22 19:15:00'),
    (5, '2026-05-25 10:00:00', '2026-05-25 10:30:08'),
    (6, '2026-05-28 13:56:12', '2026-05-28 17:01:40'),
    (7, '2026-05-30 21:00:00', '2026-05-31 01:37:22');
