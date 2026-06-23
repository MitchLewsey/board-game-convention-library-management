from lib.db import db
from lib.play import Play
from sqlalchemy import func

class PlayRepository:

    def __init__(self):
        pass

    def create(self, play: Play) -> Play:
        db.session.add(play)
        db.session.commit()
        return play
    
    def close(self, play: Play) -> Play:
        play.end_time = func.now()
        play.duration_minutes = func.floor(
            func.extract('epoch', func.now() - Play.start_time) / 60)
        db.session.commit()
        db.session.refresh(play)
        return play
    
    def find_open(self, player_id: int, board_game_id: int) -> Play | None:
        return db.session.execute(
            db.select(Play).where(
                Play.checked_out_by_player_id == player_id,
                Play.board_game_id == board_game_id,
                Play.end_time.is_(None)
            )).scalar_one_or_none()


