from src.core.exceptions import RoomAlreadyExistsException, RoomNotFoundException
from src.infra.db.models.room import Room
from src.infra.db.uow import UnitOfWork


class RoomService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_by_id(self, room_id: int) -> Room:
        async with self.uow:
            room = await self.uow.room_repository.get_by_id(room_id)
            if not room:
                raise RoomNotFoundException(f"Room not found with id: {room_id}")
            return room

    async def get_by_name(self, name: str) -> Room:
        async with self.uow:
            room = await self.uow.room_repository.get_by_name(name)
            if not room:
                raise RoomNotFoundException(f"Room not found with name: {name}")
            return room

    async def get_all(self) -> list[Room]:
        async with self.uow:
            rooms = await self.uow.room_repository.get_all()
            return rooms

    async def create(self, name: str, rows: int, columns: int) -> Room:
        async with self.uow:
            existing_room = await self.uow.room_repository.get_by_name(name)
            if existing_room:
                raise RoomAlreadyExistsException(
                    f"Room already exists with name: {name}"
                )
            room = Room(name=name, rows=rows, columns=columns)
            await self.uow.room_repository.create(room)
            return room

    async def delete(self, room_id: int) -> None:
        async with self.uow:
            room = await self.uow.room_repository.get_by_id(room_id)
            if not room:
                raise RoomNotFoundException(f"Room not found with id: {room_id}")
            await self.uow.room_repository.delete(room)