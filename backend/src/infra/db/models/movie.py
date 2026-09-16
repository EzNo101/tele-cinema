from sqlalchemy.orm import Mapped, relationship

from src.infra.db.base import Base
from src.infra.db.models.mixins import CreatedAtMixin, IdMixin


class Movie(Base, CreatedAtMixin, IdMixin):
    title: Mapped[str]
    poster_key: Mapped[str]
    duration: Mapped[int]
    genre: Mapped[str]

    sessions = relationship(
        "MovieSession", back_populates="movie", cascade="all, delete-orphan"
    )
