import pytest
from lib.exceptions import DuplicateUPCError, InvalidBaseGameError
from lib.board_game import BoardGame
from lib.board_game_repository import BoardGameRepository


@pytest.fixture
def seed_board_games(db):
    db.session.add_all([
        BoardGame(name="Pinched!",       bgg_id=450685, factory_upc="5350705999709",  min_players=2, max_players=5, min_time=45, max_time=60,  publisher="Mighty Boards, Lucky Duck Games", designer="Jonathan Gilmour-Long, David Gordon (I)", artist="Max Kosek, Vesna 'vesner' Redesiuk",        is_expansion=False),
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
        BoardGame(id=1, name="Pinched!",       bgg_id=450685, factory_upc="5350705999709",  min_players=2, max_players=5, min_time=45, max_time=60,  publisher="Mighty Boards, Lucky Duck Games", designer="Jonathan Gilmour-Long, David Gordon (I)", artist="Max Kosek, Vesna 'vesner' Redesiuk",        is_expansion=False, base_game_id=None),
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

def test_create_board_game(db, seed_board_games):
    repo = BoardGameRepository()
    board_game = BoardGame(
        name="Ark Nova",
        bgg_id=342942,
        factory_upc="0850000576407",
        min_players=1,
        max_players=4,
        min_time=90,
        max_time=150,
        publisher="Feuerland Spiele, Capstone Games",
        designer="Mathias Wigge",
        artist="Steffen Bieker, Loïc Billiau, Dennis Lohausen",
        is_expansion=False,
        base_game_id=None
        )
    repo.create(board_game)

    db.session.close()

    ark_nova = repo.find_by_upc("0850000576407")
    assert ark_nova == BoardGame(
        id=8,
        name="Ark Nova",
        bgg_id=342942,
        factory_upc="0850000576407",
        min_players=1,
        max_players=4,
        min_time=90,
        max_time=150,
        publisher="Feuerland Spiele, Capstone Games",
        designer="Mathias Wigge",
        artist="Steffen Bieker, Loïc Billiau, Dennis Lohausen",
        is_expansion=False,
        base_game_id=None
        )
    
def test_create_board_game_with_duplicate_upc_raises_error(db, seed_board_games):
    repo = BoardGameRepository()
    duplicate_board_game = BoardGame(
        name="Catan Dupe",
        bgg_id=999,
        factory_upc="029877030415",
        min_players=6,
        max_players=9,
        min_time=99,
        max_time=999,
        publisher="KOSMOS dupe",
        designer="Klaus Teuber dupe",
        artist="Michael Menzel dupe",
        is_expansion=False,
        base_game_id=None
        )
    
    with pytest.raises(DuplicateUPCError) as e:  
        repo.create(duplicate_board_game)
    error_message = str(e.value)

    assert error_message == f"Duplicate UPC ({duplicate_board_game.factory_upc}) already exists for game {duplicate_board_game.name}"

def test_create_expansion_linked_to_base_game(db, seed_board_games):
    repo = BoardGameRepository()
    res_arcana = BoardGame(
    name="Res Arcana",
    bgg_id=262712,
    factory_upc="850004236116",
    min_players=2,
    max_players=4,
    min_time=30,
    max_time=60,
    publisher="Sand Castle Games",
    designer="Thomas Lehmann",
    artist="Julien Delval",
    is_expansion=False,
    base_game_id=None
    )
    repo.create(res_arcana)

    expansion = BoardGame(
    name="Perlae Imperii",
    bgg_id=262712,
    factory_upc="850004236550",
    min_players=2,
    max_players=4,
    min_time=30,
    max_time=60,
    publisher="Sand Castle Games",
    designer="Thomas Lehmann",
    artist="Julien Delval",
    is_expansion=True,
    base_game_id=res_arcana.id
    )
    repo.create(expansion)

    db.session.close()

    base_game = repo.find_by_upc("850004236116")
    base_game_expansion = repo.find_by_upc("850004236550")

    assert base_game_expansion.base_game_id == base_game.id

def test_create_expansion_with_invalid_base_game_errors(db, seed_board_games):
    repo = BoardGameRepository()

    expansion = BoardGame(
    name="Perlae Imperii",
    bgg_id=262712,
    factory_upc="850004236550",
    min_players=2,
    max_players=4,
    min_time=30,
    max_time=60,
    publisher="Sand Castle Games",
    designer="Thomas Lehmann",
    artist="Julien Delval",
    is_expansion=True,
    base_game_id=8
    )

    with pytest.raises(InvalidBaseGameError) as e:
        repo.create(expansion)

    error_message = str(e.value)

    assert error_message == f"Base game with ID {expansion.base_game_id} does not exist. The expansion has not been added"

def test_find_by_name_single_result(db, seed_board_games):
    repo = BoardGameRepository()
    game = repo.find_by_name("Pinched!")

    assert game[0].name == "Pinched!"
    assert game[0].factory_upc == "5350705999709"

def test_find_by_name_multiple_results(db, seed_board_games):
    repo = BoardGameRepository()
    games = repo.find_by_name("an")

    assert games[0].name == "Catan"
    assert games[1].name == "Pandemic"
    assert games[2].name == "Wingspan"

def test_find_by_name_insensitive_to_case(db, seed_board_games):
    repo = BoardGameRepository()
    games = repo.find_by_name("An")

    assert games[0].name == "Catan"
    assert games[1].name == "Pandemic"
    assert games[2].name == "Wingspan"







