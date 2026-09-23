from datetime import UTC, datetime, timedelta

from src.core.exceptions import (
    MovieNotFoundException,
    MovieSessionAlreadyExistsException,
    MovieSessionNotFoundException,
)
from src.infra.db.models.movie_session import MovieSession
from src.infra.db.uow import UnitOfWork


class MovieSessionService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_by_id(self, session_id: int) -> MovieSession:
        async with self.uow:
            session = await self.uow.movie_session_repository.get_by_id(session_id)
            if not session:
                raise MovieSessionNotFoundException(
                    f"Movie session not found with id: {session_id}"
                )
            return session

    async def get_by_movie_id(self, movie_id: int) -> list[MovieSession]:
        async with self.uow:
            sessions = await self.uow.movie_session_repository.get_by_movie_id(movie_id)
            return sessions

    async def get_by_room_id(self, room_id: int) -> list[MovieSession]:
        async with self.uow:
            sessions = await self.uow.movie_session_repository.get_by_room_id(room_id)
            return sessions

    async def create(
        self,
        movie_id: int,
        room_id: int,
        start_time: datetime,
        price_stars: int,
    ) -> MovieSession:
        async with self.uow:
            movie = await self.uow.movie_repository.get_by_id(movie_id)
            if not movie:
                raise MovieNotFoundException(f"Movie not found with id: {movie_id}")

            start = self._to_utc(start_time)
            new_end = start + timedelta(minutes=movie.duration)

            busy = await self.uow.movie_session_repository.get_by_room_id(room_id)

            durations = {
                movie.id: movie.duration
                for movie in await self.uow.movie_repository.get_all()
            }

            for session in busy:
                session_end = session.start_time + timedelta(
                    minutes=durations[session.movie_id]
                )
                if start < session_end and new_end > session.start_time:
                    raise MovieSessionAlreadyExistsException(
                        f"Movie session already exists for movie {movie_id} in room {room_id} at {start}"
                    )
            session = MovieSession(
                movie_id=movie_id,
                room_id=room_id,
                start_time=start,
                price_stars=price_stars,
            )
            await self.uow.movie_session_repository.create(session)
            return session

    @staticmethod
    def _to_utc(value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)

    async def delete(self, session_id: int) -> None:
        async with self.uow:
            session = await self.uow.movie_session_repository.get_by_id(session_id)
            if not session:
                raise MovieSessionNotFoundException(
                    f"Movie session not found with id: {session_id}"
                )
            await self.uow.movie_session_repository.delete(session)
