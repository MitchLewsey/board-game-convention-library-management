from lib.models import BoardGame
from decimal import Decimal


def test_board_game_has_correct_attributes(db):
    game = BoardGame(
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
        avg_rating=7.15,
    )
    db.session.add(game)
    db.session.commit()

    saved = db.session.get(BoardGame, game.id)

    assert saved.name == "Pinched!"
    assert saved.bgg_id == 450685
    assert saved.min_players == 2
    assert saved.max_players == 5
    assert saved.min_time == 45
    assert saved.max_time == 60
    assert saved.publisher == "Mighty Boards, Lucky Duck Games"
    assert saved.designer == "Jonathan Gilmour-Long, David Gordon (I)"
    assert saved.artist == "Max Kosek, Vesna 'vesner' Redesiuk"
    assert saved.is_expansion is False
    assert float(saved.avg_rating) == 7.15
