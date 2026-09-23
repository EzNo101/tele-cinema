from fastapi import APIRouter, HTTPException, status

from src.api.schemas.room import RoomCreate, RoomResponse
from src.core.dependencies import RoomServiceDependency
from src.core.exceptions import RoomAlreadyExistsException, RoomNotFoundException

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/{room_id}", response_model=RoomResponse, status_code=status.HTTP_200_OK)
async def get_by_id(room_id: int, room_service: RoomServiceDependency):
    """
    Get a room by its ID.
    """
    try:
        room = await room_service.get_by_id(room_id)
    except RoomNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with ID {room_id} not found.",
        ) from e
    return room


@router.get(
    "/name/{name}", response_model=RoomResponse, status_code=status.HTTP_200_OK
)
async def get_by_name(name: str, room_service: RoomServiceDependency):
    """
    Get a room by its name.
    """
    try:
        room = await room_service.get_by_name(name)
    except RoomNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with name {name} not found.",
        ) from e
    return room


@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def create(room: RoomCreate, room_service: RoomServiceDependency):
    """
    Create a new room.
    """
    try:
        new_room = await room_service.create(
            name=room.name,
            rows=room.rows,
            columns=room.columns,
        )
    except RoomAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Room with name {room.name} already exists.",
        ) from e
    return new_room


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(room_id: int, room_service: RoomServiceDependency):
    """
    Delete a room by its ID.
    """
    try:
        await room_service.delete(room_id)
    except RoomNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with ID {room_id} not found.",
        ) from e
