from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.models.booking import Booking, BookingStatus
from src.infra.db.repositories.base import BaseRepository


class BookingRepository(BaseRepository[Booking]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Booking)

    async def get_by_user_id(self, user_id: int) -> list[Booking]:
        result = await self.session.execute(
            select(Booking).where(Booking.user_id == user_id)
        )
        return list(result.scalars().all())

    async def get_by_seat_id(self, seat_id: int) -> list[Booking]:
        result = await self.session.execute(
            select(Booking).where(Booking.seat_id == seat_id)
        )
        return list(result.scalars().all())

    async def update_status(
        self, booking_id: int, status: BookingStatus
    ) -> Booking | None:
        booking = await self.session.get(Booking, booking_id)
        if not booking:
            return None
        booking.status = status
        return booking
