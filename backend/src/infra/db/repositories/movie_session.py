from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.models.movie_session import MovieSession
from src.infra.db.repositories.base import BaseRepository


class MovieSessionRepository(BaseRepository[MovieSession]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, MovieSession)

    async def get_by_movie_id(self, movie_id: int) -> list[MovieSession]:
        result = await self.session.execute(
            self.model.__table__.select().where(self.model.movie_id == movie_id)
        )
        return list(result.scalars().all())

    async def get_by_room_id(self, room_id: int) -> list[MovieSession]:
        result = await self.session.execute(
            self.model.__table__.select().where(self.model.room_id == room_id)
        )
        return list(result.scalars().all())
