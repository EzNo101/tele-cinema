from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.models.movie_session import MovieSession


class MovieSessionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, session_id: int) -> MovieSession | None:
        return await self.session.get(MovieSession, session_id)

    async def get_all(self) -> list[MovieSession]:
        result = await self.session.execute(select(MovieSession))
        return list(result.scalars().all())

    async def create(self, movie_session: MovieSession) -> MovieSession:
        self.session.add(movie_session)
        return movie_session

    async def delete(self, movie_session: MovieSession) -> None:
        await self.session.delete(movie_session)
