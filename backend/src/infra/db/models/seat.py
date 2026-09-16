from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.db.base import Base
from src.infra.db.models.mixins import IdMixin


class Seat(Base, IdMixin):
    __table_args__ = (UniqueConstraint("session_id", "row", "number"),)
    session_id: Mapped[int] = mapped_column(
        ForeignKey(
            "moviesession.id",
            ondelete="CASCADE",
        )
    )
    row: Mapped[int]
    number: Mapped[int]

    bookings = relationship(
        "Booking",
        back_populates="seat",
        cascade="all, delete-orphan",
    )
