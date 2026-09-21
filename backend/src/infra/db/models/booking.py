from enum import Enum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.db.base import Base
from src.infra.db.models.mixins import CreatedAtMixin, IdMixin, UpdatedAtMixin


class BookingStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"


class Booking(Base, IdMixin, CreatedAtMixin, UpdatedAtMixin):
    session_id: Mapped[int] = mapped_column(
        ForeignKey("moviesession.id", ondelete="CASCADE")
    )
    seat_id: Mapped[int] = mapped_column(
        ForeignKey(
            "seat.id",
            ondelete="CASCADE",
        )
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "appuser.id",
            ondelete="CASCADE",
        )
    )
    price_stars: Mapped[int]
    status: Mapped[BookingStatus] = mapped_column(
        SqlEnum(BookingStatus, name="booking_status"),
        default=BookingStatus.PENDING,
        nullable=False,
    )
    user = relationship("AppUser", back_populates="bookings")
    seat = relationship("Seat", back_populates="bookings")
