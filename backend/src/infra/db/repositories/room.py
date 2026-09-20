from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.models.room import Room
from src.infra.db.repositories.base import BaseRepository


class RoomRepository(BaseRepository[Room]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Room)

    async def get_by_name(self, name: str) -> Room | None:
        result = await self.session.execute(
            select(self.model).where(self.model.name == name)
        )
        return result.scalars().first()
