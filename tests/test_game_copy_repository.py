import pytest
from lib.game_copy import GameCopy
from lib.game_copy_repository import GameCopyRepository
from lib.board_game import BoardGame

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

def test_all_returns_all_game_copies(db, seed_board_games_game_copies):
    repo = GameCopyRepository()
    copies = repo.all()
    assert copies == [
        GameCopy(id=1,  board_game_id=1,    availability_status="Available",    condition="Good",       notes="Slightly faded",                 shelf_location="A1"),
        GameCopy(id=2,  board_game_id=1,    availability_status="Available",    condition="Fair",       notes="Box breaking, damaged cards",    shelf_location="A1"),
        GameCopy(id=3,  board_game_id=2,    availability_status="Maintenance",  condition="Poor",       notes="Missing tokens",                 shelf_location="B2"),
        GameCopy(id=4,  board_game_id=3,    availability_status="In Play",      condition="Excellent",  notes="",                               shelf_location="C4"),
        GameCopy(id=5,  board_game_id=3,    availability_status="In Play",      condition="Excellent",  notes="",                               shelf_location="C4"),
        GameCopy(id=6,  board_game_id=3,    availability_status="Maintenance",  condition="Poor",       notes="Box broken",                     shelf_location="C4"),
        GameCopy(id=7,  board_game_id=3,    availability_status="Available",    condition="Excellent",  notes="Brand new",                      shelf_location="C4")
    ]

def test_create_game_copy(db, seed_board_games_game_copies):
    repo = GameCopyRepository()
    game_copy = GameCopy(id=8,  board_game_id=2,    availability_status="Available",  condition="Excellent",       notes="New",                 shelf_location="B2")
    created_copy = repo.create(game_copy)
    assert len(repo.all()) == 8
    assert repo.all()[7].board_game_id == 2
    assert repo.all()[7].availability_status == "Available"
    assert created_copy == game_copy

def test_count_available_copies_returns_correctly_number_of_available_copies(db, seed_board_games_game_copies):
    repo = GameCopyRepository()
    assert repo.count_available(1) == 2
    assert repo.count_available(2) == 0
    assert repo.count_available(3) == 1

def test_find_available_returns_single_copy(db, seed_board_games_game_copies):
    repo = GameCopyRepository()
    available_games_copies = repo.find_available(3)
    assert available_games_copies == [
        GameCopy(id=7,  board_game_id=3,    availability_status="Available",    condition="Excellent",  notes="Brand new",                      shelf_location="C4")
        ]

def test_find_available_returns_multiple_copies(db, seed_board_games_game_copies):
    repo = GameCopyRepository()
    available_games_copies = repo.find_available(1)
    assert available_games_copies == [
        GameCopy(id=1,  board_game_id=1,    availability_status="Available",    condition="Good",       notes="Slightly faded",                 shelf_location="A1"),
        GameCopy(id=2,  board_game_id=1,    availability_status="Available",    condition="Fair",       notes="Box breaking, damaged cards",    shelf_location="A1")
        ]

def test_find_available_returns_empty_list_if_none_available(db, seed_board_games_game_copies):
    repo = GameCopyRepository()
    available_games_copies = repo.find_available(2)
    assert available_games_copies == []

def test_find_maintenance_copies(db, seed_board_games_game_copies):
    repo = GameCopyRepository()
    maintenance_games_copies = repo.find_maintenance()
    assert maintenance_games_copies == [
        GameCopy(id=3,  board_game_id=2,    availability_status="Maintenance",  condition="Poor",       notes="Missing tokens",                 shelf_location="B2"),
        GameCopy(id=6,  board_game_id=3,    availability_status="Maintenance",  condition="Poor",       notes="Box broken",                     shelf_location="C4")
    ]

def test_set_status_flags_copy_for_maintenance(db, seed_board_games_game_copies):
    repo = GameCopyRepository()
    flagged_copy = repo.set_status(1, "Maintenance", "Missing 3 cards")
    assert flagged_copy.availability_status == "Maintenance"
    assert flagged_copy.notes == "Missing 3 cards"
    assert len(repo.find_maintenance()) == 3

def test_set_status_returns_copy_to_available(db, seed_board_games_game_copies):
    repo = GameCopyRepository()
    flagged_copy = repo.set_status(3, "Available", "Tokens replaced")
    assert flagged_copy.availability_status == "Available"
    assert flagged_copy.notes == "Tokens replaced"
    assert len(repo.find_maintenance()) == 1
