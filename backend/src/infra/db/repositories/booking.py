from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.models.booking import Booking, BookingStatus


class BookingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, booking_id: int) -> Booking | None:
        return await self.session.get(Booking, booking_id)

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

    async def get_all(self) -> list[Booking]:
        result = await self.session.execute(select(Booking))
        return list(result.scalars().all())

    async def create(self, booking: Booking) -> Booking:
        self.session.add(booking)
        return booking

    async def update_status(
        self, booking_id: int, status: BookingStatus
    ) -> Booking | None:
        booking = await self.session.get(Booking, booking_id)
        if not booking:
            return None
        booking.status = status
        return booking

    async def delete(self, booking: Booking) -> None:
        await self.session.delete(booking)
