from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.models.seat import Seat
from src.infra.db.repositories.base import BaseRepository


class SeatRepository(BaseRepository[Seat]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Seat)

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
