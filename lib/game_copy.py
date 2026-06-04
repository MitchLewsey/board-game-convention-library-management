import enum

from sqlalchemy.orm import Mapped, mapped_column

from lib.db import db


class AvailabilityStatus(str, enum.Enum):
    AVAILABLE = 'Available'
    IN_PLAY = 'In Play'
    MAINTENANCE = 'Maintenance'


class CopyCondition(str, enum.Enum):
    EXCELLENT = 'Excellent'
    GOOD = 'Good'
    FAIR = 'Fair'
    POOR = 'Poor'


class GameCopy(db.Model):
    __tablename__ = 'game_copy'

    id: Mapped[int] = mapped_column(primary_key=True)
    board_game_id: Mapped[int] = mapped_column(
        db.ForeignKey('board_game.id', ondelete='CASCADE'), nullable=False)
    availability_status: Mapped[AvailabilityStatus] = mapped_column(
        db.Enum(AvailabilityStatus, name='availability_status',
                values_callable=lambda e: [m.value for m in e]),
        nullable=False, default=AvailabilityStatus.AVAILABLE)
    condition: Mapped[CopyCondition | None] = mapped_column(
        db.Enum(CopyCondition, name='copy_condition',
                values_callable=lambda e: [m.value for m in e]))
    notes: Mapped[str | None] = mapped_column(db.Text)
    shelf_location: Mapped[str | None] = mapped_column(db.String(50))

    def __eq__(self, other):
        if not isinstance(other, GameCopy):
            return NotImplemented
        copy1 = {k: v for k, v in self.__dict__.items() if k != '_sa_instance_state'}
        copy2 = {k: v for k, v in other.__dict__.items() if k != '_sa_instance_state'}
        return copy1 == copy2

    def __repr__(self):
        return f"GameCopy({self.id}, {self.board_game_id}, {self.availability_status}, {self.condition}, {self.notes}, {self.shelf_location})"
