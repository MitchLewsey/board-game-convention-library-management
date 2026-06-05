from lib.db import db
from lib.game_copy import GameCopy
from sqlalchemy import func

class GameCopyRepository:

    def __init__(self):
        pass

    def all(self) -> list[GameCopy]:
        return list(db.session.execute(
            db.select(GameCopy))
            .scalars()
            .all()
            
            )
    
    def create(self, game_copy) -> None:
        db.session.add(game_copy)
        db.session.commit()
        return None
    
    def count_available(self, board_game_id) -> int:
        return db.session.execute(
            db.select(func.count())
            .select_from(GameCopy)
            .where(
                GameCopy.board_game_id == board_game_id,
                GameCopy.availability_status == 'Available'
            )
        ).scalar_one()
    
