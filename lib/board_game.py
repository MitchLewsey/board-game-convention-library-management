from sqlalchemy.orm import Mapped, mapped_column

from lib.db import db


class BoardGame(db.Model):
    __tablename__ = 'board_game'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    bgg_id: Mapped[int | None] = mapped_column(db.Integer)
    factory_upc: Mapped[str | None] = mapped_column(db.String(20), unique=True)
    min_players: Mapped[int | None] = mapped_column(db.SmallInteger)
    max_players: Mapped[int | None] = mapped_column(db.SmallInteger)
    min_time: Mapped[int | None] = mapped_column(db.SmallInteger)
    max_time: Mapped[int | None] = mapped_column(db.SmallInteger)
    publisher: Mapped[str | None] = mapped_column(db.String(255))
    designer: Mapped[str | None] = mapped_column(db.String(255))
    artist: Mapped[str | None] = mapped_column(db.String(255))
    is_expansion: Mapped[bool] = mapped_column(db.Boolean, nullable=False, default=False)
    base_game_id: Mapped[int | None] = mapped_column(
        db.ForeignKey('board_game.id', ondelete='SET NULL'))

    def __eq__(self, other):
        game1 = {k: v for k, v in self.__dict__.items() if k != '_sa_instance_state'}
        game2 = {k: v for k, v in other.__dict__.items() if k != '_sa_instance_state'}
        return game1 == game2
    
    def __repr__(self):
        return f"BoardGame({self.id}, {self.name}, {self.bgg_id}, {self.factory_upc}, {self.min_players}, {self.max_players}, {self.min_time}, {self.max_time}, {self.publisher}, {self.designer}, {self.artist}, {self.is_expansion}, {self.base_game_id})"