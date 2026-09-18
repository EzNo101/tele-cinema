from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.models.movie import Movie


class MovieRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, movie_id: int) -> Movie | None:
        return await self.session.get(Movie, movie_id)

    async def get_all(self) -> list[Movie]:
        result = await self.session.execute(select(Movie))
        return list(result.scalars().all())

    async def create(self, movie: Movie) -> Movie:
        self.session.add(movie)
        return movie

    async def delete(self, movie: Movie) -> None:
        await self.session.delete(movie)
