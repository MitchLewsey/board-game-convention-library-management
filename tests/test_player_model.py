from lib.player import Player

"""
Player constructs with all related attributes
"""

def test_player_constructs():
    player = Player(
        id=1,
        alias="ace"
    )

    assert player.id == 1
    assert player.alias == "ace"

def test_two_players_are_equal():
    player_1 = Player(
        id=1,
        alias="ace"
    )

    player_2 = Player(
        id=1,
        alias="ace"
    )

    assert player_1 == player_2

def test_stringify_player():
    player = Player(
        id=1,
        alias="ace"
    )

    assert str(player) == "Player(1, ace)"
