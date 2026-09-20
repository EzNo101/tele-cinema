from src.core.exceptions import RoomAlreadyExistsException, RoomNotFoundException
from src.infra.db.models.room import Room
from src.infra.db.uow import UnitOfWork


class RoomService:
    async def get_by_id(self, room_id: int, uow: UnitOfWork) -> Room:
        async with uow:
            room = await uow.room_repository.get_by_id(room_id)
            if not room:
                raise RoomNotFoundException(f"Room not found with id: {room_id}")
            return room

    async def get_by_name(self, name: str, uow: UnitOfWork) -> Room:
        async with uow:
            room = await uow.room_repository.get_by_name(name)
            if not room:
                raise RoomNotFoundException(f"Room not found with name: {name}")
            return room

    async def get_all(self, uow: UnitOfWork) -> list[Room]:
        async with uow:
            rooms = await uow.room_repository.get_all()
            return rooms

    async def create(self, name: str, rows: int, columns: int, uow: UnitOfWork) -> Room:
        async with uow:
            existing_room = await uow.room_repository.get_by_name(name)
            if existing_room:
                raise RoomAlreadyExistsException(f"Room already exists with id: {name}")
            room = Room(name=name, rows=rows, columns=columns)
            await uow.room_repository.create(room)
            return room

    async def delete(self, room_id: int, uow: UnitOfWork) -> None:
        async with uow:
            room = await uow.room_repository.get_by_id(room_id)
            if not room:
                raise RoomNotFoundException(f"Room not found with id: {room_id}")
            await uow.room_repository.delete(room)
