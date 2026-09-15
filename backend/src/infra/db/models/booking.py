from enum import Enum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.db.base import Base


class BookingStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"


class Booking(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    seat_id: Mapped[int] = mapped_column(
        ForeignKey(
            "seat.id",
            ondelete="CASCADE",
        )
    )
    status: Mapped[BookingStatus] = mapped_column(
        SqlEnum(BookingStatus, name="booking_status"),
        default=BookingStatus.PENDING,
        nullable=False,
    )
