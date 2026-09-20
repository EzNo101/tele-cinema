from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.db.base import Base
from src.infra.db.models.mixins import CreatedAtMixin, IdMixin


class MovieSession(Base, CreatedAtMixin, IdMixin):
    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.id", ondelete="CASCADE"))
    room_id: Mapped[int] = mapped_column(ForeignKey("room.id", ondelete="CASCADE"))
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    price_stars: Mapped[int]

    movie = relationship("Movie", back_populates="sessions")
    room = relationship("Room", back_populates="sessions")
