from datetime import UTC, datetime, timedelta

from src.core.exceptions import (
    MovieNotFoundException,
    MovieSessionAlreadyExistsException,
    MovieSessionNotFoundException,
)
from src.infra.db.models.movie_session import MovieSession
from src.infra.db.uow import UnitOfWork


class MovieSessionService:
    async def get_by_id(self, session_id: int, uow: UnitOfWork) -> MovieSession:
        async with uow:
            session = await uow.movie_session_repository.get_by_id(session_id)
            if not session:
                raise MovieSessionNotFoundException(
                    f"Movie session not found with id: {session_id}"
                )
            return session

    async def get_by_movie_id(
        self,
        movie_id: int,
        uow: UnitOfWork,
    ) -> list[MovieSession]:
        async with uow:
            sessions = await uow.movie_session_repository.get_by_movie_id(movie_id)
            return sessions

    async def create(
        self,
        movie_id: int,
        room_id: int,
        start_time: datetime,
        price_stars: int,
        uow: UnitOfWork,
    ) -> MovieSession:
        async with uow:
            movie = await uow.movie_repository.get_by_id(movie_id)
            if not movie:
                raise MovieNotFoundException(f"Movie not found with id: {movie_id}")

            start = self._to_utc(start_time)
            new_end = start + timedelta(minutes=movie.duration)

            busy = await uow.movie_session_repository.get_by_room_id(room_id)

            durations = {
                movie.id: movie.duration
                for movie in await uow.movie_repository.get_all()
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
            await uow.movie_session_repository.create(session)
            return session

    @staticmethod
    def _to_utc(value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)

    async def delete(self, session_id: int, uow: UnitOfWork) -> None:
        async with uow:
            session = await uow.movie_session_repository.get_by_id(session_id)
            if not session:
                raise MovieSessionNotFoundException(
                    f"Movie session not found with id: {session_id}"
                )
            await uow.movie_session_repository.delete(session)
