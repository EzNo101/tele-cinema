from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.models.app_user import AppUser


class AppUserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> AppUser | None:
        return await self.session.get(AppUser, user_id)

    async def get_all(self) -> list[AppUser]:
        result = await self.session.execute(select(AppUser))
        return list(result.scalars().all())

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

    async def create(self, user: AppUser) -> AppUser:
        self.session.add(user)
        return user

    async def delete(self, user: AppUser) -> None:
        await self.session.delete(user)
