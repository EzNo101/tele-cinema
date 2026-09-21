from typing import Annotated

from fastapi import Depends

from src.infra.db.uow import UnitOfWork
from src.services.app_user import AppUserService
from src.services.booking import BookingService
from src.services.movie import MovieService
from src.services.movie_session import MovieSessionService
from src.services.room import RoomService
from src.services.seat import SeatService


def get_uow() -> UnitOfWork:
    return UnitOfWork()


UnitOfWorkDependency = Annotated[UnitOfWork, Depends(get_uow)]


def get_app_user_service(
    uow: UnitOfWorkDependency,
) -> AppUserService:
    return AppUserService(uow)


def get_booking_service(
    uow: UnitOfWorkDependency,
) -> BookingService:
    return BookingService(uow)


def get_movie_service(
    uow: UnitOfWorkDependency,
) -> MovieService:
    return MovieService(uow)


def get_movie_session_service(
    uow: UnitOfWorkDependency,
) -> MovieSessionService:
    return MovieSessionService(uow)


def get_room_service(
    uow: UnitOfWorkDependency,
) -> RoomService:
    return RoomService(uow)


def get_seat_service(
    uow: UnitOfWorkDependency,
) -> SeatService:
    return SeatService(uow)


AppUserServiceDependency = Annotated[AppUserService, Depends(get_app_user_service)]
BookingServiceDependency = Annotated[BookingService, Depends(get_booking_service)]
MovieServiceDependency = Annotated[MovieService, Depends(get_movie_service)]
MovieSessionServiceDependency = Annotated[
    MovieSessionService,
    Depends(get_movie_session_service),
]

RoomServiceDependency = Annotated[RoomService, Depends(get_room_service)]
SeatServiceDependency = Annotated[SeatService, Depends(get_seat_service)]
