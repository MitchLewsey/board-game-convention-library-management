# Database Design Recipe

## User Stories

As a board game convention owner,
So I can optimise my board game library,
I want to be able to log every time a game is played and how much fun the player(s) had via a rating.

As a board game convention owner,
So I can ensure our games are in a playable state,
I want to be able to monitor the condition of the game.

As a board game convention owner,
So I can locate missing games,
I want to be able to know who most recently checked out a game and where they are.

As a board game convention owner,
So I can manage multiple copies of the same game,
I want to be able to store multiple, identical games and each one has it's own availability, location, condition etc.

As a board game convention owner,
So I can ensure all games are in a playable state
I want players to be able to mark the condition of a copy and add custom notes (e.g. missing pieces etc.)

As a board game convention owner,
So I can manage the games in my library easily,
I want to be able to the library to my BoardGameGeek (bgg) games list.

As a board game convention attendee,
So I can see what games I like and what games to buy,
I want to be able to see all the games I've played and what rating I gave them.

As a board game convention attendee,
So I can check out games quickly,
I want to be able to search the board game library for a specific game and find it's shelf location and availability (checked in/checked out).

As a board game convention attendee,
So I can pick a game to play to suit my situation,
I want to be able to see all of the games currently available based on specific filterable criteria (play time (mins), min player count, max player count, type (coop/competitive), mechanisms)..

As a board game convention attendee,
So I can log all the details of the games I played,
I want to be able to add multiple players to a play, the winner, play time and how we all rated the game

As a board game convention attendee,
So I can quickly check-out a game,
I want to be able to scan the UPC on the box.

As a board game convention owner or attendee,
So I can correctly log plays and manage the library,
I want to be able to log games as 'expansions' and associate 'expansions' with another game.

As a board game convention owner or attendee,
So I can differentiate different versions of games,
I want to be able to see the designer, artist and release year.

### Nouns:

game library, game, convention owner, convention attendee, condition, shelf location, condition, rating/score, availability (checked in/checked out), type (coop/competitive), mechanism, min player count, max player count, play time (mins), designer, artist and release year, expansion, play, winner, UPC, notes

## Table Names and Columns

| Tables                | Columns             |
| --------------------- | ------------------  |
| board_game            |id, name, bgg_id, min_players, max_players, min_time, max_time, publisher, designer, artist, is_expansion, base_game_id
| game_copy             | id, board_game_id, factory_upc, availability_status, condition, notes, shelf_location
| player                | id, name, alias
| play                  | id, board_game_id, date_played, duration minutes
| play_participant      | play_id, player_id, is_winner, rating

## Table & Column Types

### board_game

Column Name     |   Type            | Details
| --------------| ------------------|------------------|
id              |   SERIAL          |   primary key
name            |   VARCHAR(255)    |   not null
bgg_id          |   INTEGER         |   
factory_upc     |   VARCHAR(20)     |   unique
min_players     |   SMALLINT        |   if blank, 1
max_players     |   SMALLINT        |
min_time        |   SMALLINT        |
publisher       |   VARCHAR(255)    |
designer        |   VARCHAR(255)    |
artist          |   VARCHAR(255)    |
is_expansion    |   BOOLEAN         |   not null, default false
base_game_id    |   INTEGER         |   references board_game(id)
avg_rating      |   NUMERIC(4, 2)   |

### game_copy
Column Name         |   Type                | Details
| ------------------| ------------------    |------------------|
id                  |   SERIAL              |   primary key
board_game_id       |   INTEGER             |   not null, references board_game(id), on delete cascade
availability_status |   availability_status |   not null, default 'Available', enum
condition           |   VARCHAR(50)         |   'Excellent', 'Good, 'Fair', 'Poor'
shelf_location      |   VARCHAR(50)         |   

### player
Column Name         |   Type            | Details
| ------------------| ------------------|------------------|
id                  |   SERIAL          | primary key
name                |   VARCHAR(255)    | 
alias               |   VARCHAR(100)    | not null

### play
Column Name         |   Type            | Details
| ------------------| ------------------|------------------|
id                  |   SERIAL          | primary key
board_game_id       |   INTEGER         | not null references board_game(id) on delete restrict
date_played         |   DATE            | not null default current_date
duration_minutes    |   SMALLINT        |
start_time          

### play_participant
Column Name         |   Type            | Details
| ------------------| ------------------|------------------|
play_id             |   INTEGER         |   not null references play(id) on delete cascade
player_id           |   INTEGER         |   not null references player(id) ON DELETE restrict
is_winner           |   BOOLEAN         |   not null default false
rating              |   SMALLINT        |   check between 1 and 10

primary key, (play_id, player_id)

