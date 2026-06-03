from lib.db import db
from lib.board_game import BoardGame


class BoardGameRepository:

    def __init__(self):
        pass

    def all(self):
        return db.session.execute(db.select(BoardGame)).scalars().all()
    
    def find_by_upc(self, factory_upc):
        return db.session.execute(db.select(BoardGame).where(BoardGame.factory_upc == factory_upc)).scalars().one_or_none()