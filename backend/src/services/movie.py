from src.core.exceptions import MovieAlreadyExistsException, MovieNotFoundException
from src.infra.db.models.movie import Movie
from src.infra.db.uow import UnitOfWork


class MovieService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_by_id(self, movie_id: int) -> Movie:
        async with self.uow:
            movie = await self.uow.movie_repository.get_by_id(movie_id)
            if not movie:
                raise MovieNotFoundException(f"Movie not found with id: {movie_id}")
            return movie

    async def get_by_id_with_sessions(self, movie_id: int) -> Movie:
        async with self.uow:
            movie = await self.uow.movie_repository.get_by_id_with_sessions(movie_id)
            if not movie:
                raise MovieNotFoundException(f"Movie not found with id: {movie_id}")
            return movie

    async def get_by_title(self, title: str) -> Movie:
        async with self.uow:
            movie = await self.uow.movie_repository.get_by_title(title)
            if not movie:
                raise MovieNotFoundException(f"Movie not found with title: {title}")
            return movie

    async def get_all(self) -> list[Movie]:
        async with self.uow:
            movies = await self.uow.movie_repository.get_all()
            return movies

    async def create(
        self, title: str, poster_key: str, duration: int, genre: str
    ) -> Movie:
        async with self.uow:
            existing_movie = await self.uow.movie_repository.get_by_title(title)
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
            await self.uow.movie_repository.create(movie)
            return movie

    async def delete(self, movie_id: int) -> None:
        async with self.uow:
            movie = await self.uow.movie_repository.get_by_id(movie_id)
            if not movie:
                raise MovieNotFoundException(f"Movie not found with id: {movie_id}")
            await self.uow.movie_repository.delete(movie)
