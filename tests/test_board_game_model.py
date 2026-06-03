from lib.board_game import BoardGame

"""
Board Game constructs with all related attributes
"""

def test_board_game_constructs():
    game = BoardGame(
        id=1,
        name="Pinched!",
        bgg_id=450685,
        factory_upc="012345678901",
        min_players=2,
        max_players=5,
        min_time=45,
        max_time=60,
        publisher="Mighty Boards, Lucky Duck Games",
        designer="Jonathan Gilmour-Long, David Gordon (I)",
        artist="Max Kosek, Vesna 'vesner' Redesiuk",
        is_expansion=False,
        base_game_id=None,
    )

    assert game.name == "Pinched!"
    assert game.bgg_id == 450685
    assert game.min_players == 2
    assert game.max_players == 5
    assert game.min_time == 45
    assert game.max_time == 60
    assert game.publisher == "Mighty Boards, Lucky Duck Games"
    assert game.designer == "Jonathan Gilmour-Long, David Gordon (I)"
    assert game.artist == "Max Kosek, Vesna 'vesner' Redesiuk"
    assert game.is_expansion is False
    assert game.base_game_id is None

def test_two_board_games_are_equal():
    game_1 = BoardGame(
        id=1,
        name="Pinched!",
        bgg_id=450685,
        factory_upc="012345678901",
        min_players=2,
        max_players=5,
        min_time=45,
        max_time=60,
        publisher="Mighty Boards, Lucky Duck Games",
        designer="Jonathan Gilmour-Long, David Gordon (I)",
        artist="Max Kosek, Vesna 'vesner' Redesiuk",
        is_expansion=False,
        base_game_id=None,
    )

    game_2 = BoardGame(
        id=1,
        name="Pinched!",
        bgg_id=450685,
        factory_upc="012345678901",
        min_players=2,
        max_players=5,
        min_time=45,
        max_time=60,
        publisher="Mighty Boards, Lucky Duck Games",
        designer="Jonathan Gilmour-Long, David Gordon (I)",
        artist="Max Kosek, Vesna 'vesner' Redesiuk",
        is_expansion=False,
        base_game_id=None,
    )

    assert game_1 == game_2

def test_stringify_board_game():
    game_1 = BoardGame(
        id=1,
        name="Pinched!",
        bgg_id=450685,
        factory_upc="012345678901",
        min_players=2,
        max_players=5,
        min_time=45,
        max_time=60,
        publisher="Mighty Boards, Lucky Duck Games",
        designer="Jonathan Gilmour-Long, David Gordon (I)",
        artist="Max Kosek, Vesna 'vesner' Redesiuk",
        is_expansion=False,
        base_game_id=None,
    )
    assert str(game_1) == "BoardGame(1, Pinched!, 450685, 012345678901, 2, 5, 45, 60, Mighty Boards, Lucky Duck Games, Jonathan Gilmour-Long, David Gordon (I), Max Kosek, Vesna 'vesner' Redesiuk, False, None)"