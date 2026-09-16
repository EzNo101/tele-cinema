from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.db.base import Base
from src.infra.db.models.mixins import CreatedAtMixin, IdMixin


class Seat(Base, IdMixin, CreatedAtMixin):
    __table_args__ = (UniqueConstraint("session_id", "row", "number"),)
    session_id: Mapped[int] = mapped_column(
        ForeignKey(
            "moviesession.id",
            ondelete="CASCADE",
        )
    )
    row: Mapped[int]
    number: Mapped[int]
