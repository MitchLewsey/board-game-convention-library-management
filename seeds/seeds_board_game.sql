-- The job of this file is to reset all of our important database tables.
-- And add any data that is needed for the tests to run.
-- This is so that our tests, and application, are always operating from a fresh
-- database state, and that tests don't interfere with each other.

TRUNCATE board_game CASCADE;

DROP TABLE IF EXISTS board_game;
DROP SEQUENCE IF EXISTS board_game_id_seq;

CREATE TYPE availability_status AS ENUM ('Available', 'In Play', 'Maintenance');
CREATE TYPE copy_condition AS ENUM ('Excellent', 'Good', 'Fair', 'Poor');

CREATE TABLE board_game (
    id              SERIAL          PRIMARY KEY,
    name            VARCHAR(255)    NOT NULL,
    bgg_id          INTEGER,                        -- BoardGameGeek ID
    factory_upc     VARCHAR(20)     UNIQUE,         -- scanned by barcode reader to identify title
    min_players     SMALLINT,
    max_players     SMALLINT,
    min_time        SMALLINT,                       -- minutes
    max_time        SMALLINT,                       -- minutes
    publisher       VARCHAR(255),
    designer        VARCHAR(255),
    artist          VARCHAR(255),
    is_expansion    BOOLEAN         NOT NULL DEFAULT FALSE,
    base_game_id    INTEGER         REFERENCES board_game(id) ON DELETE SET NULL,
    avg_rating      NUMERIC(4, 2)   CHECK (avg_rating BETWEEN 0 AND 10)
);

INSERT INTO board_game (name, bgg_id, factory_upc, min_players, max_players, min_time, max_time, publisher, designer, artist, is_expansion, avg_rating)
VALUES
    ('Pinched!',        450685, '012345678901',  2, 5, 45,  60,  'Mighty Boards, Lucky Duck Games', 'Jonathan Gilmour-Long, David Gordon (I)', 'Max Kosek, Vesna ''vesner'' Redesiuk',                  FALSE, 7.15),
    ('Catan',           13,     '029877030415',  3, 4, 60,  120, 'KOSMOS',                          'Klaus Teuber',                            'Michael Menzel',                                        FALSE, 7.15),
    ('Ticket to Ride',  9209,   '824968717912',  2, 5, 45,  75,  'Days of Wonder',                  'Alan R. Moon',                            'Julien Delval, Cyrille Daujean',                        FALSE, 7.41),
    ('Pandemic',        30549,  '681706711003',  2, 4, 45,  60,  'Z-Man Games',                     'Matt Leacock',                            'Christian Hanisch, Josh Cappel',                        FALSE, 7.61),
    ('Codenames',       178900, '8594156310012', 2, 8, 15,  30,  'Czech Games Edition',             'Vlaada Chvatil',                          'Stasha Kolibanova',                                     FALSE, 7.73),
    ('Azul',            230802, '826956600528',  2, 4, 30,  45,  'Next Move Games',                 'Michael Kiesling',                        'Chris Quilliams',                                       FALSE, 7.78),
    ('Wingspan',        266192, '850000576428',  1, 5, 40,  70,  'Stonemaier Games',                'Elizabeth Hargrave',                      'Ana Maria Martinez Jaramillo, Natalia Rojas, Beth Sobel', FALSE, 8.01);
