from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.models.app_user import AppUser
from src.infra.db.repositories.base import BaseRepository


class AppUserRepository(BaseRepository[AppUser]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AppUser)

    async def get_by_telegram_id(self, telegram_id: int) -> AppUser | None:
        result = await self.session.execute(
            select(AppUser).where(AppUser.telegram_id == telegram_id)
        )
        return result.scalars().first()

    async def get_by_username(self, username: str) -> AppUser | None:
        result = await self.session.execute(
            select(AppUser).where(AppUser.username == username)
        )
        return result.scalars().first()
