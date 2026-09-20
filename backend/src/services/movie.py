from src.core.exceptions import MovieAlreadyExistsException, MovieNotFoundException
from src.infra.db.models.movie import Movie
from src.infra.db.uow import UnitOfWork


class MovieService:
    async def get_by_id(self, movie_id: int, uow: UnitOfWork) -> Movie:
        async with uow:
            movie = await uow.movie_repository.get_by_id(movie_id)
            if not movie:
                raise MovieNotFoundException(f"Movie not found with id: {movie_id}")
            return movie

    async def get_by_title(self, title: str, uow: UnitOfWork) -> Movie:
        async with uow:
            movie = await uow.movie_repository.get_by_title(title)
            if not movie:
                raise MovieNotFoundException(f"Movie not found with title: {title}")
            return movie

    async def create(
        self, title: str, poster_key: str, duration: int, genre: str, uow: UnitOfWork
    ) -> Movie:
        async with uow:
            existing_movie = await uow.movie_repository.get_by_title(title)
            if existing_movie:
                raise MovieAlreadyExistsException(
                    f"Movie already exists with title: {title}"
                )
            movie = Movie(
                title=title,
                poster_key=poster_key,
                duration=duration,
                genre=genre,
            )
            await uow.movie_repository.create(movie)
            return movie

    async def delete(self, movie_id: int, uow: UnitOfWork) -> None:
        async with uow:
            movie = await uow.movie_repository.get_by_id(movie_id)
            if not movie:
                raise MovieNotFoundException(f"Movie not found with id: {movie_id}")
            await uow.movie_repository.delete(movie)
