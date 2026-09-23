from fastapi import APIRouter, HTTPException, status

from src.api.schemas.seat import SeatCreate, SeatResponse
from src.core.dependencies import SeatServiceDependency
from src.core.exceptions import SeatAlreadyExistsException, SeatNotFoundException

router = APIRouter(prefix="/seats", tags=["Seats"])


@router.get("/{seat_id}", response_model=SeatResponse, status_code=status.HTTP_200_OK)
async def get_by_id(seat_id: int, seat_service: SeatServiceDependency):
    """
    Get a seat by its ID.
    """
    try:
        seat = await seat_service.get_by_id(seat_id)
    except SeatNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Seat with ID {seat_id} not found.",
        ) from e
    return seat


@router.get(
    "/{row}/{column}", response_model=SeatResponse, status_code=status.HTTP_200_OK
)
async def get_by_row_and_column(
    row: int,
    column: int,
    session_id: int,
    seat_service: SeatServiceDependency,
):
    """
    Get a seat by its row and column.
    """
    try:
        seat = await seat_service.get_by_row_and_column(
            session_id=session_id,
            row=row,
            column=column,
        )
    except SeatNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Seat at row {row} and column {column} not found.",
        ) from e
    return seat


@router.post("/", response_model=SeatResponse, status_code=status.HTTP_201_CREATED)
async def create(seat_create: SeatCreate, seat_service: SeatServiceDependency):
    """
    Create a new seat.
    """
    try:
        seat = await seat_service.create(
            session_id=seat_create.session_id,
            row=seat_create.row,
            column=seat_create.column,
        )
    except SeatAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Seat already exists at row {seat_create.row} and column {seat_create.column}.",
        ) from e
    return seat


@router.delete("/{seat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(seat_id: int, seat_service: SeatServiceDependency):
    """
    Delete a seat by its ID.
    """
    try:
        await seat_service.delete(seat_id)
    except SeatNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Seat with ID {seat_id} not found.",
        ) from e
