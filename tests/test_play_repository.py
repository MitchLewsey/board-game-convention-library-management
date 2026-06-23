import pytest
from datetime import datetime
from lib.game_copy import GameCopy
from lib.board_game import BoardGame
from lib.play import Play
from lib.play_repository import PlayRepository

@pytest.fixture
def seed_board_games_game_copies(db):
    db.session.add_all([
        BoardGame(name="Pinched!",       bgg_id=450685, factory_upc="5350705999709",  min_players=2, max_players=5, min_time=45, max_time=60,  publisher="Mighty Boards, Lucky Duck Games", designer="Jonathan Gilmour-Long, David Gordon (I)", artist="Max Kosek, Vesna 'vesner' Redesiuk",        is_expansion=False),
        BoardGame(name="Catan",          bgg_id=13,     factory_upc="029877030415",  min_players=3, max_players=4, min_time=60, max_time=120, publisher="KOSMOS",                          designer="Klaus Teuber",                            artist="Michael Menzel",                           is_expansion=False),
        BoardGame(name="Ticket to Ride", bgg_id=9209,   factory_upc="824968717912",  min_players=2, max_players=5, min_time=45, max_time=75,  publisher="Days of Wonder",                  designer="Alan R. Moon",                            artist="Julien Delval, Cyrille Daujean",            is_expansion=False),
        BoardGame(name="Pandemic",       bgg_id=30549,  factory_upc="681706711003",  min_players=2, max_players=4, min_time=45, max_time=60,  publisher="Z-Man Games",                     designer="Matt Leacock",                            artist="Christian Hanisch, Josh Cappel",            is_expansion=False),
        BoardGame(name="Codenames",      bgg_id=178900, factory_upc="8594156310012", min_players=2, max_players=8, min_time=15, max_time=30,  publisher="Czech Games Edition",             designer="Vlaada Chvatil",                          artist="Stasha Kolibanova",                        is_expansion=False),
        BoardGame(name="Azul",           bgg_id=230802, factory_upc="826956600528",  min_players=2, max_players=4, min_time=30, max_time=45,  publisher="Next Move Games",                 designer="Michael Kiesling",                        artist="Chris Quilliams",                          is_expansion=False),
        BoardGame(name="Wingspan",       bgg_id=266192, factory_upc="850000576428",  min_players=1, max_players=5, min_time=40, max_time=70,  publisher="Stonemaier Games",                designer="Elizabeth Hargrave",                      artist="Ana Maria Martinez Jaramillo, Natalia Rojas, Beth Sobel", is_expansion=False),
        GameCopy(id=1,  board_game_id=1,    availability_status="Available",    condition="Good",       notes="Slightly faded",                 shelf_location="A1"),
        GameCopy(id=2,  board_game_id=1,    availability_status="Available",    condition="Fair",       notes="Box breaking, damaged cards",    shelf_location="A1"),
        GameCopy(id=3,  board_game_id=2,    availability_status="Maintenance",  condition="Poor",       notes="Missing tokens",                 shelf_location="B2"),
        GameCopy(id=4,  board_game_id=3,    availability_status="In Play",      condition="Excellent",  notes="",                               shelf_location="C4"),
        GameCopy(id=5,  board_game_id=3,    availability_status="In Play",      condition="Excellent",  notes="",                               shelf_location="C4"),
        GameCopy(id=6,  board_game_id=3,    availability_status="Maintenance",  condition="Poor",       notes="Box broken",                     shelf_location="C4"),
        GameCopy(id=7,  board_game_id=3,    availability_status="Available",    condition="Excellent",  notes="Brand new",                      shelf_location="C4")
    ])
    db.session.commit()

def test_create_play(db, seed_board_games_game_copies):
    play_repo = PlayRepository()
    play = Play(board_game_id=2)
    play_repo.create(play)
    assert play.id is not None
    assert play.start_time is not None
    assert play.end_time is None
    assert play.duration_minutes is None

def test_find_open_play(db, seed_board_games_game_copies):
    play_repo = PlayRepository()
    play = Play(board_game_id=2)
    play_repo.create(play)
    play_repo.find_open(board_game_id=2, checked_out_by_player_id=1)
        