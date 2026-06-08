from datetime import datetime, timedelta
from lib.play import Play

"""
Play constructs with all related attributes
"""

def test_play_constructs():
    play = Play(
        id=1,
        board_game_id=2,
        start_time=datetime(2026, 6, 5, 00, 30, 0),
        end_time=datetime(2026, 6, 5, 00, 55, 0),
        duration_minutes=25
    )

    assert play.id == 1
    assert play.board_game_id == 2
    assert play.start_time == datetime(2026, 6, 5, 00, 30, 0)
    assert play.end_time == datetime(2026, 6, 5, 00, 55, 0)
    assert play.duration_minutes == 25


