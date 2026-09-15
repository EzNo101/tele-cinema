from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.db.base import Base


class Seat(Base):
    __table_args__ = (UniqueConstraint("session_id", "row", "number"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey(
            "moviesession.id",
            ondelete="CASCADE",
        )
    )
    row: Mapped[int]
    number: Mapped[int]
