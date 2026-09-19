from src.core.exceptions import UserAlreadyExistsException, UserNotFoundException
from src.infra.db.models.app_user import AppUser
from src.infra.db.uow import UnitOfWork


class AppUserService:
    async def get_by_telegram_id(self, telegram_id: int, uow: UnitOfWork) -> AppUser:
        async with uow:
            user = await uow.app_user_repository.get_by_telegram_id(telegram_id)
            if not user:
                raise UserNotFoundException(
                    f"User not found with telegram_id: {telegram_id}"
                )
            return user

    async def get_by_id(self, user_id: int, uow: UnitOfWork) -> AppUser:
        async with uow:
            user = await uow.app_user_repository.get_by_id(user_id)
            if not user:
                raise UserNotFoundException(f"User not found with id: {user_id}")
            return user

    async def get_by_username(self, username: str, uow: UnitOfWork) -> AppUser:
        async with uow:
            user = await uow.app_user_repository.get_by_username(username)
            if not user:
                raise UserNotFoundException(f"User not found with username: {username}")
            return user

    async def get_all(self, uow: UnitOfWork) -> list[AppUser]:
        async with uow:
            users = await uow.app_user_repository.get_all()
            return users

    async def create(self, telegram_id: int, username: str, uow: UnitOfWork) -> AppUser:
        async with uow:
            existing_user = await uow.app_user_repository.get_by_telegram_id(
                telegram_id
            )
            if existing_user:
                raise UserAlreadyExistsException(
                    f"User already exists with telegram_id: {telegram_id}"
                )
            user = AppUser(telegram_id=telegram_id, username=username)
            await uow.app_user_repository.create(user)
            return user

    async def delete(self, user_id: int, uow: UnitOfWork) -> None:
        async with uow:
            user = await uow.app_user_repository.get_by_id(user_id)
            if not user:
                raise UserNotFoundException(f"User not found with id: {user_id}")
            await uow.app_user_repository.delete(user)
