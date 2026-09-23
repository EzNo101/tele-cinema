from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.models.seat import Seat
from src.infra.db.repositories.base import BaseRepository


class SeatRepository(BaseRepository[Seat]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Seat)

    async def get_by_row_and_column(
        self, session_id: int, row: int, column: int
    ) -> Seat | None:
        result = await self.session.execute(
            select(Seat).where(
                Seat.session_id == session_id,
                Seat.row == row,
                Seat.column == column,
            )
        )
        return result.scalars().first()

    async def get_by_session_id(self, session_id: int) -> list[Seat]:
        result = await self.session.execute(
            select(Seat).where(Seat.session_id == session_id)
        )
        return list(result.scalars().all())
