from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.db.base import Base


class Movie(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    image: Mapped[str]
    duration: Mapped[int]
    genre: Mapped[str]

    sessions = relationship(
        "MovieSession", back_populates="movie", cascade="all, delete-orphan"
    )
