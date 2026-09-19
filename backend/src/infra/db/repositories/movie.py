from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.models.movie import Movie
from src.infra.db.repositories.base import BaseRepository


class MovieRepository(BaseRepository[Movie]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Movie)
