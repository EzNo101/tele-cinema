from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories import *
from src.infra.db.session import AsyncSessionLocal


class UnitOfWork:
    def __init__(self):
        self.session: AsyncSession | None
        self.app_user_repository: AppUserRepository
        self.booking_repository: BookingRepository
        self.movie_repository: MovieRepository
        self.movie_session_repository: MovieSessionRepository
        self.seat_repository: SeatRepository

    async def __aenter__(self):
        self.session = AsyncSessionLocal()
        self.app_user_repository = AppUserRepository(self.session)
        self.booking_repository = BookingRepository(self.session)
        self.movie_repository = MovieRepository(self.session)
        self.movie_session_repository = MovieSessionRepository(self.session)
        self.seat_repository = SeatRepository(self.session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_traceback: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
        assert self.session is not None
        await self.session.close()

    async def commit(self) -> None:
        assert self.session is not None
        await self.session.commit()

    async def rollback(self) -> None:
        assert self.session is not None
        await self.session.rollback()
