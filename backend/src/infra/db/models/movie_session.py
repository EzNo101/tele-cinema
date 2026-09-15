from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.db.base import Base


class MovieSession(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.id", ondelete="CASCADE"))
    start_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    price_stars: Mapped[int]

    movie = relationship("Movie", back_populates="sessions")
