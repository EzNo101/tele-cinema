from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.infra.db.models.movie import Movie
from src.infra.db.repositories.base import BaseRepository


class MovieRepository(BaseRepository[Movie]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Movie)

    async def get_by_title(self, title: str) -> Movie | None:
        result = await self.session.execute(
            self.model.__table__.select().where(self.model.title == title)
        )
        return result.scalar_one_or_none()

    async def get_all_sessions(self, movie_id: int) -> Movie | None:
        result = await self.session.execute(
            select(Movie)
            .options(selectinload(Movie.sessions))
            .where(Movie.id == movie_id)
        )
        return result.scalar_one_or_none()
