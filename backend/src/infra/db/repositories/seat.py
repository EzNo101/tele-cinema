from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.models.seat import Seat


class SeatRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, seat_id: int) -> Seat | None:
        return await self.session.get(Seat, seat_id)

    async def get_by_row_and_number(
        self, session_id: int, row: int, number: int
    ) -> Seat | None:
        result = await self.session.execute(
            select(Seat).where(
                Seat.session_id == session_id,
                Seat.row == row,
                Seat.number == number,
            )
        )
        return result.scalars().first()

    async def get_by_session_id(self, session_id: int) -> list[Seat]:
        result = await self.session.execute(
            select(Seat).where(Seat.session_id == session_id)
        )
        return list(result.scalars().all())

    async def get_all(self) -> list[Seat]:
        result = await self.session.execute(select(Seat))
        return list(result.scalars().all())

    async def create(self, seat: Seat) -> Seat:
        self.session.add(seat)
        return seat

    async def delete(self, seat: Seat) -> None:
        await self.session.delete(seat)
