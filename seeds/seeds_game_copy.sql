TRUNCATE game_copy;

INSERT INTO game_copy (board_game_id, availability_status, condition, shelf_location)
VALUES
    ((SELECT id FROM board_game WHERE name = 'Pinched!'),       'Available'::availability_status,   'Excellent'::copy_condition, 'A1'),
    ((SELECT id FROM board_game WHERE name = 'Catan'),          'Available'::availability_status,   'Good'::copy_condition,      'A2'),
    ((SELECT id FROM board_game WHERE name = 'Catan'),          'Available'::availability_status,   'Good'::copy_condition,      'A2'),
    ((SELECT id FROM board_game WHERE name = 'Ticket to Ride'), 'Available'::availability_status,   'Excellent'::copy_condition, 'B1'),
    ((SELECT id FROM board_game WHERE name = 'Ticket to Ride'), 'In Play'::availability_status,     'Good'::copy_condition,      'B1'),
    ((SELECT id FROM board_game WHERE name = 'Pandemic'),       'Available'::availability_status,   'Good'::copy_condition,      'B2'),
    ((SELECT id FROM board_game WHERE name = 'Codenames'),      'Available'::availability_status,   'Excellent'::copy_condition, 'C1'),
    ((SELECT id FROM board_game WHERE name = 'Codenames'),      'Available'::availability_status,   'Fair'::copy_condition,      'C1'),
    ((SELECT id FROM board_game WHERE name = 'Azul'),           'In Play'::availability_status,     'Excellent'::copy_condition, 'C2'),
    ((SELECT id FROM board_game WHERE name = 'Wingspan'),       'Available'::availability_status,   'Good'::copy_condition,      'D1'),
    ((SELECT id FROM board_game WHERE name = 'Wingspan'),       'Maintenance'::availability_status, 'Poor'::copy_condition,      'D1');

UPDATE game_copy
SET notes = 'Missing 3 bird cards'
WHERE board_game_id = (SELECT id FROM board_game WHERE name = 'Wingspan')
  AND availability_status = 'Maintenance'::availability_status;
