from lib.db import db
from lib.game_copy import GameCopy
from lib.board_game import BoardGame
from sqlalchemy import func

class GameCopyRepository:

    def __init__(self):
        pass

    def all(self) -> list[GameCopy]:
        return list(db.session.execute(
            db.select(GameCopy))
            .scalars().all())
    
    def create(self, game_copy) -> GameCopy:
        db.session.add(game_copy)
        db.session.commit()
        return game_copy
    
    def count_available(self, board_game_id) -> int:
        return db.session.execute(
            db.select(func.count())
            .select_from(GameCopy)
            .where(
                GameCopy.board_game_id == board_game_id,
                GameCopy.availability_status == 'Available'
            )
        ).scalar_one()
    
    def find_available(self, board_game_id: int) -> list[GameCopy]:
        return list(
            db.session.execute(
            db.select(GameCopy).
            where(
                GameCopy.board_game_id == board_game_id,
                GameCopy.availability_status == 'Available'
            )
        ).scalars().all()
        )
    
    def find_maintenance(self) -> list[GameCopy]:
        return list(
            db.session.execute(
            db.select(GameCopy).
            where(
                GameCopy.availability_status == 'Maintenance'
            )
        ).scalars().all()
        )

    def set_status(self, copy_id, status, notes) -> GameCopy:
        game_copy = db.session.get(GameCopy, copy_id)
        game_copy.availability_status = status
        game_copy.notes = notes
        db.session.commit()
        return game_copy

