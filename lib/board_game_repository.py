from lib.db import db
from lib.board_game import BoardGame
from sqlalchemy.exc import IntegrityError
from lib.exceptions import DuplicateUPCError, InvalidBaseGameError


class BoardGameRepository:

    def __init__(self):
        pass

    def all(self) -> list[BoardGame]:
        return list(db.session.execute(db.select(BoardGame)).scalars().all())
    
    def find_by_upc(self, factory_upc: str) -> BoardGame | None:
        return db.session.execute(db.select(BoardGame).where(BoardGame.factory_upc == factory_upc)).scalars().one_or_none()
    
    def find_by_name(self, name: str) -> list[BoardGame]:
        return list(db.session.execute(db.select(BoardGame).where(BoardGame.name.ilike(f"%{name}%"))).scalars().all())
    
    def find_by_id(self, id: int) -> BoardGame | None:
        return db.session.execute(db.select(BoardGame).where(BoardGame.id == id)).scalars().one_or_none()
    
    def create(self, board_game: BoardGame) -> None | str:
        if board_game.is_expansion is True:
            if not BoardGameRepository().find_by_id(board_game.base_game_id):
                raise InvalidBaseGameError(f"Base game with ID {board_game.base_game_id} does not exist. The expansion has not been added")
        try:
            db.session.add(board_game)
            db.session.commit()
            return None
        except IntegrityError:
            db.session.rollback()
            raise DuplicateUPCError(f"Duplicate UPC ({board_game.factory_upc}) already exists for game {board_game.name}")