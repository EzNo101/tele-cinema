from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.models.movie_session import MovieSession
from src.infra.db.repositories.base import BaseRepository


class MovieSessionRepository(BaseRepository[MovieSession]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, MovieSession)
