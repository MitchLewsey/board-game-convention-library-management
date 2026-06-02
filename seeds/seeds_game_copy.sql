-- The job of this file is to reset all of our important database tables.
-- And add any data that is needed for the tests to run.
-- This is so that our tests, and application, are always operating from a fresh
-- database state, and that tests don't interfere with each other.

TRUNCATE board_game CASCADE;

DROP TABLE IF EXISTS game_copy;
DROP SEQUENCE IF EXISTS game_copy_id_seq;

CREATE TABLE game_copy (
    id                  SERIAL              PRIMARY KEY,
    board_game_id       INTEGER             NOT NULL REFERENCES board_game(id) ON DELETE CASCADE,
    availability_status availability_status NOT NULL DEFAULT 'Available',
    condition           copy_condition,
    notes               TEXT,
    shelf_location      VARCHAR(50)
);


INSERT INTO game_copy (board_game_id, availability_status, condition, notes, shelf_location)
VALUES
    ((SELECT id FROM board_game WHERE name = 'Pinched!'),       'Available'::availability_status,   'Excellent'::copy_condition, NULL,                   'A1'),
    ((SELECT id FROM board_game WHERE name = 'Catan'),          'Available'::availability_status,   'Good'::copy_condition,      NULL,                   'A2'),
    ((SELECT id FROM board_game WHERE name = 'Catan'),          'Available'::availability_status,   'Good'::copy_condition,      NULL,                   'A2'),
    ((SELECT id FROM board_game WHERE name = 'Ticket to Ride'), 'Available'::availability_status,   'Excellent'::copy_condition, NULL,                   'B1'),
    ((SELECT id FROM board_game WHERE name = 'Ticket to Ride'), 'In Play'::availability_status,     'Good'::copy_condition,      NULL,                   'B1'),
    ((SELECT id FROM board_game WHERE name = 'Pandemic'),       'Available'::availability_status,   'Good'::copy_condition,      NULL,                   'B2'),
    ((SELECT id FROM board_game WHERE name = 'Codenames'),      'Available'::availability_status,   'Excellent'::copy_condition, NULL,                   'C1'),
    ((SELECT id FROM board_game WHERE name = 'Codenames'),      'Available'::availability_status,   'Fair'::copy_condition,      NULL,                   'C1'),
    ((SELECT id FROM board_game WHERE name = 'Azul'),           'In Play'::availability_status,     'Excellent'::copy_condition, NULL,                   'C2'),
    ((SELECT id FROM board_game WHERE name = 'Wingspan'),       'Available'::availability_status,   'Good'::copy_condition,      NULL,                   'D1'),
    ((SELECT id FROM board_game WHERE name = 'Wingspan'),       'Maintenance'::availability_status, 'Poor'::copy_condition,      'Missing 3 bird cards', 'D1');
