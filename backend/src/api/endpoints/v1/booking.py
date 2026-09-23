from fastapi import APIRouter, HTTPException, status

from src.api.schemas.booking import BookingCreate, BookingResponse, BookingUpdateStatus
from src.core.dependencies import BookingServiceDependency
from src.core.exceptions import (
    BookingAlreadyExistsException,
    BookingNotFoundException,
    MovieSessionNotFoundException,
    SeatNotFoundException,
    UserNotFoundException,
)

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get(
    "/{booking_id}",
    response_model=BookingResponse,
    status_code=status.HTTP_200_OK,
)
async def get_by_id(booking_id: int, booking_service: BookingServiceDependency):
    """
    Get a booking by its ID.
    """
    try:
        booking = await booking_service.get_by_id(booking_id)
    except BookingNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with ID {booking_id} not found.",
        ) from e
    return booking


@router.get(
    "/user/{user_id}",
    response_model=list[BookingResponse],
    status_code=status.HTTP_200_OK,
)
async def get_by_user_id(user_id: int, booking_service: BookingServiceDependency):
    """
    Get all bookings for a user.
    """
    try:
        bookings = await booking_service.get_by_user_id(user_id)
    except BookingNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bookings for user {user_id} not found.",
        ) from e
    return bookings


@router.get(
    "/seat/{seat_id}",
    response_model=list[BookingResponse],
    status_code=status.HTTP_200_OK,
)
async def get_by_seat_id(seat_id: int, booking_service: BookingServiceDependency):
    """
    Get all bookings for a seat.
    """
    try:
        bookings = await booking_service.get_by_seat_id(seat_id)
    except BookingNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bookings for seat {seat_id} not found.",
        ) from e
    return bookings


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create(
    booking_create: BookingCreate, booking_service: BookingServiceDependency
):
    """
    Create a new booking.
    """
    try:
        booking = await booking_service.create(
            user_id=booking_create.user_id,
            seat_id=booking_create.seat_id,
        )
    except BookingAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Booking already exists for user {booking_create.user_id} and seat {booking_create.seat_id}.",
        ) from e
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {booking_create.user_id} not found.",
        ) from e
    except SeatNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Seat with ID {booking_create.seat_id} not found.",
        ) from e
    except MovieSessionNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie session not found.",
        ) from e
    return booking


@router.patch(
    "/{booking_id}/status",
    response_model=BookingResponse,
    status_code=status.HTTP_200_OK,
)
async def update_status(
    booking_id: int,
    booking_status: BookingUpdateStatus,
    booking_service: BookingServiceDependency,
):
    """
    Update the status of a booking.
    """
    try:
        booking = await booking_service.update_status(booking_id, booking_status.status)
    except BookingNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with ID {booking_id} not found.",
        ) from e
    return booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(booking_id: int, booking_service: BookingServiceDependency):
    """
    Delete a booking by its ID.
    """
    try:
        await booking_service.delete(booking_id)
    except BookingNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with ID {booking_id} not found.",
        ) from e
