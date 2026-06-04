from lib.db import db
from lib.board_game import BoardGame
from sqlalchemy.exc import IntegrityError


class BoardGameRepository:

    def __init__(self):
        pass

    def all(self):
        return db.session.execute(db.select(BoardGame)).scalars().all()
    
    def find_by_upc(self, factory_upc):
        return db.session.execute(db.select(BoardGame).where(BoardGame.factory_upc == factory_upc)).scalars().one_or_none()
    
    def create(self, board_game):
        try:
            db.session.add(board_game)
            db.session.commit()
            return None
        except IntegrityError:
            db.session.rollback()
            return f"Duplicate UPC ({board_game.factory_upc}) - {board_game.name} already exists"