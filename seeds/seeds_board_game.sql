TRUNCATE board_game CASCADE;

INSERT INTO board_game (name, bgg_id, factory_upc, min_players, max_players, min_time, max_time, publisher, designer, artist, is_expansion, avg_rating)
VALUES
    ('Pinched!',        450685, '012345678901',  2, 5, 45,  60,  'Mighty Boards, Lucky Duck Games', 'Jonathan Gilmour-Long, David Gordon (I)', 'Max Kosek, Vesna ''vesner'' Redesiuk',                  FALSE, 7.15),
    ('Catan',           13,     '029877030415',  3, 4, 60,  120, 'KOSMOS',                          'Klaus Teuber',                            'Michael Menzel',                                        FALSE, 7.15),
    ('Ticket to Ride',  9209,   '824968717912',  2, 5, 45,  75,  'Days of Wonder',                  'Alan R. Moon',                            'Julien Delval, Cyrille Daujean',                        FALSE, 7.41),
    ('Pandemic',        30549,  '681706711003',  2, 4, 45,  60,  'Z-Man Games',                     'Matt Leacock',                            'Christian Hanisch, Josh Cappel',                        FALSE, 7.61),
    ('Codenames',       178900, '8594156310012', 2, 8, 15,  30,  'Czech Games Edition',             'Vlaada Chvatil',                          'Stasha Kolibanova',                                     FALSE, 7.73),
    ('Azul',            230802, '826956600528',  2, 4, 30,  45,  'Next Move Games',                 'Michael Kiesling',                        'Chris Quilliams',                                       FALSE, 7.78),
    ('Wingspan',        266192, '850000576428',  1, 5, 40,  70,  'Stonemaier Games',                'Elizabeth Hargrave',                      'Ana Maria Martinez Jaramillo, Natalia Rojas, Beth Sobel', FALSE, 8.01);
