import pytest
from lib.exceptions import DuplicateAliasError
from lib.player import Player
from lib.player_repository import PlayerRepository


@pytest.fixture
def seed_players(db):
    db.session.add_all([
        Player(alias="ali"),
        Player(alias="bobby"),
        Player(alias="chaz"),
    ])
    db.session.commit()


def test_create_player_with_duplicate_alias_raises_error(db, seed_players):
    repo = PlayerRepository()
    duplicate_player = Player(alias="ali")

    with pytest.raises(DuplicateAliasError) as e:
        repo.create(duplicate_player)
    error_message = str(e.value)

    assert error_message == f"Duplicate alias ({duplicate_player.alias}) already exists"
