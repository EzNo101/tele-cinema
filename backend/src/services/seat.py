from src.core.exceptions import (
    SeatAlreadyExistsException,
    SeatNotFoundException,
)
from src.infra.db.models import Seat
from src.infra.db.uow import UnitOfWork


class SeatService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_by_id(self, seat_id: int) -> Seat:
        async with self.uow:
            seat = await self.uow.seat_repository.get_by_id(seat_id)
            if not seat:
                raise SeatNotFoundException(f"Seat not found with id: {seat_id}")
            return seat

    async def get_by_row_and_number(
        self,
        session_id: int,
        row: int,
        number: int,
    ) -> Seat:
        async with self.uow:
            seat = await self.uow.seat_repository.get_by_row_and_number(
                session_id, row, number
            )
            if not seat:
                raise SeatNotFoundException(
                    f"Seat not found in session {session_id} at row {row}, number {number}"
                )
            return seat

    async def get_by_session_id(self, session_id: int) -> list[Seat]:
        async with self.uow:
            seats = await self.uow.seat_repository.get_by_session_id(session_id)
            return seats

    async def get_all(self) -> list[Seat]:
        async with self.uow:
            seats = await self.uow.seat_repository.get_all()
            return seats

    async def create(
        self,
        session_id: int,
        row: int,
        number: int,
    ) -> Seat:
        async with self.uow:
            existing_seat = await self.uow.seat_repository.get_by_row_and_number(
                session_id,
                row,
                number,
            )
            if existing_seat:
                raise SeatAlreadyExistsException(
                    f"Seat already exists in session {session_id} at row {row}, number {number}"
                )

            new_seat = Seat(session_id=session_id, row=row, number=number)
            await self.uow.seat_repository.create(new_seat)
            return new_seat

    async def delete(self, seat_id: int) -> None:
        async with self.uow:
            seat = await self.uow.seat_repository.get_by_id(seat_id)
            if not seat:
                raise SeatNotFoundException(f"Seat not found with id: {seat_id}")
            await self.uow.seat_repository.delete(seat)