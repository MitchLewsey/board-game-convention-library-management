from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from lib.db import db
from datetime import datetime

class Play(db.Model):
    __tablename__ = 'play'

    id: Mapped[int] = mapped_column(primary_key=True)
    board_game_id: Mapped[int] = mapped_column(
        db.ForeignKey('board_game.id', ondelete='RESTRICT'), nullable=False)
    checked_out_by_player_id: Mapped[int | None] = mapped_column(
        db.ForeignKey('player.id', ondelete='RESTRICT'))
    start_time: Mapped[datetime] = mapped_column(server_default=func.now())
    end_time: Mapped[datetime | None]
    duration_minutes: Mapped[int | None] = mapped_column(db.SmallInteger)

    def __eq__(self, other):
        play1 = {k: v for k, v in self.__dict__.items() if k != '_sa_instance_state'}
        play2 = {k: v for k, v in other.__dict__.items() if k != '_sa_instance_state'}
        return play1 == play2
    
    def __repr__(self):
        return f"Play({self.id}, {self.board_game_id}, {self.checked_out_by_player_id}, {self.start_time}, {self.end_time}, {self.duration_minutes})"


