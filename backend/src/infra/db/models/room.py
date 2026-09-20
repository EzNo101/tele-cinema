from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.db.base import Base
from src.infra.db.models.mixins import CreatedAtMixin, IdMixin, UpdatedAtMixin


class Room(Base, IdMixin, CreatedAtMixin, UpdatedAtMixin):
    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    rows: Mapped[int] = mapped_column(nullable=False)
    columns: Mapped[int] = mapped_column(nullable=False)

    sessions = relationship(
        "MovieSession",
        back_populates="room",
        cascade="all, delete-orphan",
    )
