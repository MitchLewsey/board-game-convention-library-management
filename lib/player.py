from sqlalchemy.orm import Mapped, mapped_column

from lib.db import db


class Player(db.Model):
    __tablename__ = 'player'

    id: Mapped[int] = mapped_column(primary_key=True)
    alias: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)

    def __eq__(self, other):
        if not isinstance(other, Player):
            return NotImplemented
        player1 = {k: v for k, v in self.__dict__.items() if k != '_sa_instance_state'}
        player2 = {k: v for k, v in other.__dict__.items() if k != '_sa_instance_state'}
        return player1 == player2

    def __repr__(self):
        return f"Player({self.id}, {self.alias})"
