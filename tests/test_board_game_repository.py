import pytest
from lib.board_game import BoardGame
from lib.board_game_repository import BoardGameRepository


@pytest.fixture
def seed_board_games(db):
    db.session.add_all([
        BoardGame(name="Pinched!",       bgg_id=450685, factory_upc="012345678901",  min_players=2, max_players=5, min_time=45, max_time=60,  publisher="Mighty Boards, Lucky Duck Games", designer="Jonathan Gilmour-Long, David Gordon (I)", artist="Max Kosek, Vesna 'vesner' Redesiuk",        is_expansion=False),
        BoardGame(name="Catan",          bgg_id=13,     factory_upc="029877030415",  min_players=3, max_players=4, min_time=60, max_time=120, publisher="KOSMOS",                          designer="Klaus Teuber",                            artist="Michael Menzel",                           is_expansion=False),
        BoardGame(name="Ticket to Ride", bgg_id=9209,   factory_upc="824968717912",  min_players=2, max_players=5, min_time=45, max_time=75,  publisher="Days of Wonder",                  designer="Alan R. Moon",                            artist="Julien Delval, Cyrille Daujean",            is_expansion=False),
        BoardGame(name="Pandemic",       bgg_id=30549,  factory_upc="681706711003",  min_players=2, max_players=4, min_time=45, max_time=60,  publisher="Z-Man Games",                     designer="Matt Leacock",                            artist="Christian Hanisch, Josh Cappel",            is_expansion=False),
        BoardGame(name="Codenames",      bgg_id=178900, factory_upc="8594156310012", min_players=2, max_players=8, min_time=15, max_time=30,  publisher="Czech Games Edition",             designer="Vlaada Chvatil",                          artist="Stasha Kolibanova",                        is_expansion=False),
        BoardGame(name="Azul",           bgg_id=230802, factory_upc="826956600528",  min_players=2, max_players=4, min_time=30, max_time=45,  publisher="Next Move Games",                 designer="Michael Kiesling",                        artist="Chris Quilliams",                          is_expansion=False),
        BoardGame(name="Wingspan",       bgg_id=266192, factory_upc="850000576428",  min_players=1, max_players=5, min_time=40, max_time=70,  publisher="Stonemaier Games",                designer="Elizabeth Hargrave",                      artist="Ana Maria Martinez Jaramillo, Natalia Rojas, Beth Sobel", is_expansion=False),
    ])
    db.session.commit()


def test_all_returns_all_board_games(db, seed_board_games):
    repo = BoardGameRepository()
    games = repo.all()
    assert games == [
        BoardGame(id=1, name="Pinched!",       bgg_id=450685, factory_upc="012345678901",  min_players=2, max_players=5, min_time=45, max_time=60,  publisher="Mighty Boards, Lucky Duck Games", designer="Jonathan Gilmour-Long, David Gordon (I)", artist="Max Kosek, Vesna 'vesner' Redesiuk",        is_expansion=False, base_game_id=None),
        BoardGame(id=2, name="Catan",          bgg_id=13,     factory_upc="029877030415",  min_players=3, max_players=4, min_time=60, max_time=120, publisher="KOSMOS",                          designer="Klaus Teuber",                            artist="Michael Menzel",                           is_expansion=False, base_game_id=None),
        BoardGame(id=3, name="Ticket to Ride", bgg_id=9209,   factory_upc="824968717912",  min_players=2, max_players=5, min_time=45, max_time=75,  publisher="Days of Wonder",                  designer="Alan R. Moon",                            artist="Julien Delval, Cyrille Daujean",            is_expansion=False, base_game_id=None),
        BoardGame(id=4, name="Pandemic",       bgg_id=30549,  factory_upc="681706711003",  min_players=2, max_players=4, min_time=45, max_time=60,  publisher="Z-Man Games",                     designer="Matt Leacock",                            artist="Christian Hanisch, Josh Cappel",            is_expansion=False, base_game_id=None),
        BoardGame(id=5, name="Codenames",      bgg_id=178900, factory_upc="8594156310012", min_players=2, max_players=8, min_time=15, max_time=30,  publisher="Czech Games Edition",             designer="Vlaada Chvatil",                          artist="Stasha Kolibanova",                        is_expansion=False, base_game_id=None),
        BoardGame(id=6, name="Azul",           bgg_id=230802, factory_upc="826956600528",  min_players=2, max_players=4, min_time=30, max_time=45,  publisher="Next Move Games",                 designer="Michael Kiesling",                        artist="Chris Quilliams",                          is_expansion=False, base_game_id=None),
        BoardGame(id=7, name="Wingspan",       bgg_id=266192, factory_upc="850000576428",  min_players=1, max_players=5, min_time=40, max_time=70,  publisher="Stonemaier Games",                designer="Elizabeth Hargrave",                      artist="Ana Maria Martinez Jaramillo, Natalia Rojas, Beth Sobel", is_expansion=False, base_game_id=None),
    ]


def test_find_board_game_by_exist_factory_upc_returns_game(db, seed_board_games):
    repo = BoardGameRepository()
    catan = repo.find_by_upc("029877030415")
    assert catan == BoardGame(
        id=2,
        name="Catan",
        bgg_id=13,
        factory_upc="029877030415",
        min_players=3,
        max_players=4,
        min_time=60,
        max_time=120,
        publisher="KOSMOS",
        designer="Klaus Teuber",
        artist="Michael Menzel",
        is_expansion=False,
        base_game_id=None
        )
    
def test_find_board_game_by_nonexistant_factory_upc_returns_none(db, seed_board_games):
    repo = BoardGameRepository()
    ark_nova = repo.find_by_upc("0850000576407")
    assert ark_nova is None


