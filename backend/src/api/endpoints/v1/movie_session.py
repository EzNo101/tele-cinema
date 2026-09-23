from fastapi import APIRouter, HTTPException, status

from src.api.schemas.movie_session import MovieSessionCreate, MovieSessionResponse
from src.core.dependencies import MovieSessionServiceDependency
from src.core.exceptions import (
    MovieSessionAlreadyExistsException,
    MovieSessionNotFoundException,
)

router = APIRouter(prefix="/movie-sessions", tags=["Movie Sessions"])


@router.get(
    "/{session_id}",
    response_model=MovieSessionResponse,
    status_code=status.HTTP_200_OK,
)
async def get_by_id(
    session_id: int, movie_session_service: MovieSessionServiceDependency
):
    """
    Get a movie session by its ID.
    """
    try:
        session = await movie_session_service.get_by_id(session_id)
    except MovieSessionNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie session with ID {session_id} not found.",
        ) from e
    return session


@router.get(
    "/movie/{movie_id}",
    response_model=list[MovieSessionResponse],
    status_code=status.HTTP_200_OK,
)
async def get_by_movie_id(
    movie_id: int, movie_session_service: MovieSessionServiceDependency
):
    """
    Get all movie sessions for a specific movie by its ID.
    """
    sessions = await movie_session_service.get_by_movie_id(movie_id)
    return sessions


@router.get(
    "/room/{room_id}",
    response_model=list[MovieSessionResponse],
    status_code=status.HTTP_200_OK,
)
async def get_by_room_id(
    room_id: int,
    movie_session_service: MovieSessionServiceDependency,
):
    """
    Get all movie sessions for a specific room by its ID.
    """
    sessions = await movie_session_service.get_by_room_id(room_id)
    return sessions


@router.post(
    "/", response_model=MovieSessionResponse, status_code=status.HTTP_201_CREATED
)
async def create(
    movie_session_create: MovieSessionCreate,
    movie_session_service: MovieSessionServiceDependency,
):
    """
    Create a new movie session.
    """
    try:
        session = await movie_session_service.create(
            movie_id=movie_session_create.movie_id,
            room_id=movie_session_create.room_id,
            start_time=movie_session_create.start_time,
            price_stars=movie_session_create.price_stars,
        )
    except MovieSessionAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Movie session already exists for movie {movie_session_create.movie_id} in room {movie_session_create.room_id} at {movie_session_create.start_time}.",
        ) from e
    return session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(session_id: int, movie_session_service: MovieSessionServiceDependency):
    """
    Delete a movie session by its ID.
    """
    try:
        await movie_session_service.delete(session_id)
    except MovieSessionNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie session with ID {session_id} not found.",
        ) from e
