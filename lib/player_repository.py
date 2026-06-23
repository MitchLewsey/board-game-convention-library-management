from lib.db import db
from lib.player import Player
from sqlalchemy.exc import IntegrityError
from lib.exceptions import DuplicateAliasError


class PlayerRepository:

    def __init__(self):
        pass

    def create(self, player: Player) -> None:
        try:
            db.session.add(player)
            db.session.commit()
            return None
        except IntegrityError:
            db.session.rollback()
            raise DuplicateAliasError(f"Duplicate alias ({player.alias}) already exists")
