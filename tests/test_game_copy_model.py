from lib.game_copy import GameCopy

"""
GameCopy constructs with all related attributes
"""

def test_game_copy_constructs():
    game_copy = GameCopy(
        id=1,
        board_game_id=2,
        availability_status="Available",
        condition="Excellent",
        notes="Brand new",
        shelf_location="A1"
    )

    assert game_copy.id == 1
    assert game_copy.board_game_id == 2
    assert game_copy.availability_status == "Available"
    assert game_copy.condition == "Excellent"
    assert game_copy.notes == "Brand new"
    assert game_copy.shelf_location == "A1"

def test_two_game_copys_are_equal():
    game_copy_1 = GameCopy(
        id=2,
        board_game_id=3,
        availability_status="In Play",
        condition="Poor",
        notes="Missing many pieces",
        shelf_location="C3"
    )

    game_copy_2 = GameCopy(
        id=2,
        board_game_id=3,
        availability_status="In Play",
        condition="Poor",
        notes="Missing many pieces",
        shelf_location="C3"
    )

    assert game_copy_1 == game_copy_2

def test_stringify_game_copy():
    game_copy = GameCopy(
        id=1,
        board_game_id=2,
        availability_status="Available",
        condition="Excellent",
        notes="Brand new",
        shelf_location="A1"
    )
    assert str(game_copy) == "GameCopy(1, 2, Available, Excellent, Brand new, A1)"