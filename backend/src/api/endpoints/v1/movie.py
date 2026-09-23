from fastapi import APIRouter, HTTPException, status

from src.api.schemas.movie import (
    MovieCreate,
    MovieResponse,
    MovieWithSessionsResponse,
)
from src.core.dependencies import MovieServiceDependency
from src.core.exceptions import MovieAlreadyExistsException, MovieNotFoundException

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/{movie_id}", response_model=MovieResponse, status_code=status.HTTP_200_OK)
async def get_by_id(movie_id: int, movie_service: MovieServiceDependency):
    """
    Get a movie by its ID.
    """
    try:
        movie = await movie_service.get_by_id(movie_id)
    except MovieNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with ID {movie_id} not found.",
        ) from e
    return movie


@router.get(
    "/{movie_id}/sessions",
    response_model=MovieWithSessionsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_by_id_with_sessions(movie_id: int, movie_service: MovieServiceDependency):
    """
    Get a movie by its ID along with its sessions.
    """
    try:
        movie = await movie_service.get_by_id_with_sessions(movie_id)
    except MovieNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with ID {movie_id} not found.",
        ) from e
    return movie


@router.get(
    "/title/{title}",
    response_model=MovieResponse,
    status_code=status.HTTP_200_OK,
)
async def get_by_title(title: str, movie_service: MovieServiceDependency):
    """
    Get a movie by its title.
    """
    try:
        movie = await movie_service.get_by_title(title)
    except MovieNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with title '{title}' not found.",
        ) from e
    return movie


@router.get("/", response_model=list[MovieResponse], status_code=status.HTTP_200_OK)
async def get_all_movies(movie_service: MovieServiceDependency):
    """
    Get all movies.
    """
    movies = await movie_service.get_all()
    return movies


@router.post("/", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
async def create_movie(
    movie_create: MovieCreate,
    movie_service: MovieServiceDependency,
):
    """
    Create a new movie.
    """
    try:
        movie = await movie_service.create(
            title=movie_create.title,
            poster_key=movie_create.poster_key,
            duration=movie_create.duration,
            genre=movie_create.genre,
        )
    except MovieAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Movie with title '{movie_create.title}' already exists.",
        ) from e
    return movie


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(movie_id: int, movie_service: MovieServiceDependency):
    """
    Delete a movie by its ID.
    """
    try:
        await movie_service.delete(movie_id)
    except MovieNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with ID {movie_id} not found.",
        ) from e
