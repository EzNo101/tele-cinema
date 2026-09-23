from fastapi import APIRouter, HTTPException, status

from src.api.schemas.app_user import AppUserCreate, AppUserResponse
from src.core.dependencies import AppUserServiceDependency
from src.core.exceptions import UserAlreadyExistsException, UserNotFoundException

router = APIRouter(prefix="/app-users", tags=["App Users"])


@router.get(
    "/{telegram_id}",
    response_model=AppUserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_app_user(telegram_id: int, app_user_service: AppUserServiceDependency):
    """
    Get an app user by their Telegram ID.
    """
    try:
        app_user = await app_user_service.get_by_telegram_id(telegram_id)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"App user with Telegram ID {telegram_id} not found.",
        ) from e
    return app_user


@router.get("/", response_model=list[AppUserResponse], status_code=status.HTTP_200_OK)
async def get_users(app_user_service: AppUserServiceDependency):
    """
    Get all app users.
    """
    app_users = await app_user_service.get_all()

    return app_users


@router.post("/", response_model=AppUserResponse, status_code=status.HTTP_201_CREATED)
async def create_app_user(
    app_user_data: AppUserCreate, app_user_service: AppUserServiceDependency
):
    """
    Create a new app user.
    """
    try:
        app_user = await app_user_service.create(
            username=app_user_data.username,
            telegram_id=app_user_data.telegram_id,
        )
    except UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="App user already exists.",
        ) from e
    return app_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_app_user(user_id: int, app_user_service: AppUserServiceDependency):
    """
    Delete an app user by their ID.
    """
    try:
        await app_user_service.delete(user_id)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"App user with ID {user_id} not found.",
        ) from e
