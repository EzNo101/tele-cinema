from src.core.exceptions import (
    BookingAlreadyExistsException,
    BookingNotFoundException,
    MovieSessionNotFoundException,
    SeatNotFoundException,
)
from src.infra.db.models import Booking
from src.infra.db.uow import UnitOfWork


class BookingService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_by_id(self, booking_id: int) -> Booking:
        async with self.uow:
            booking = await self.uow.booking_repository.get_by_id(booking_id)
            if not booking:
                raise BookingNotFoundException(
                    f"Booking not found with id: {booking_id}"
                )
            return booking

    async def get_by_user_id(self, user_id: int) -> list[Booking]:
        async with self.uow:
            bookings = await self.uow.booking_repository.get_by_user_id(user_id)
            return bookings

    async def get_all(self) -> list[Booking]:
        async with self.uow:
            bookings = await self.uow.booking_repository.get_all()
            return bookings

    async def get_by_seat_id(self, seat_id: int) -> list[Booking]:
        async with self.uow:
            bookings = await self.uow.booking_repository.get_by_seat_id(seat_id)
            return bookings

    async def create(self, seat_id: int, user_id: int) -> Booking:
        async with self.uow:
            existing_booking = await self.uow.booking_repository.get_by_seat_id(seat_id)
            if existing_booking:
                raise BookingAlreadyExistsException(
                    f"Booking already exists for seat {seat_id}"
                )
            seat = await self.uow.seat_repository.get_by_id(seat_id)
            if not seat:
                raise SeatNotFoundException(f"Seat not found with id: {seat_id}")

            session = await self.uow.movie_session_repository.get_by_id(seat.session_id)
            if not session:
                raise MovieSessionNotFoundException(
                    f"Session not found with id: {seat.session_id}"
                )

            booking = Booking(
                seat_id=seat.id,
                session_id=seat.session_id,
                user_id=user_id,
                price_stars=session.price_stars,
            )
            await self.uow.booking_repository.create(booking)
            return booking

    async def delete(self, booking_id: int) -> None:
        async with self.uow:
            booking = await self.uow.booking_repository.get_by_id(booking_id)
            if not booking:
                raise BookingNotFoundException(
                    f"Booking not found with id: {booking_id}"
                )
            await self.uow.booking_repository.delete(booking)