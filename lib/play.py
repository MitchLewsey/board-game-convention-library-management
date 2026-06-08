from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from lib.db import db
from datetime import datetime

class Play(db.Model):
    __tablename__ = 'play'

    id: Mapped[int] = mapped_column(primary_key=True)
    board_game_id: Mapped[int] = mapped_column(
        db.ForeignKey('board_game.id', ondelete='RESTRICT'), nullable=False)
    start_time: Mapped[datetime] = mapped_column(server_default=func.now())
    end_time: Mapped[datetime | None]
    duration_minutes: Mapped[int | None] = mapped_column(db.SmallInteger)
