from sqlalchemy import BigInteger, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.db.base import Base
from src.infra.db.models.mixins import CreatedAtMixin, IdMixin, UpdatedAtMixin


class AppUser(Base, IdMixin, CreatedAtMixin, UpdatedAtMixin):
    __table_args__ = (UniqueConstraint("telegram_id"),)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[str | None] = mapped_column(nullable=True)

    bookings = relationship(
        "Booking",
        back_populates="user",
        cascade="all, delete-orphan",
    )
