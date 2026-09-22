from pydantic import BaseModel, ConfigDict, Field


class AppUserCreate(BaseModel):
    telegram_id: int = Field(..., description="Telegram ID of the user")
    username: str | None = Field(None, description="Username of the user")


class AppUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="ID of the user")
    telegram_id: int = Field(..., description="Telegram ID of the user")
    username: str | None = Field(None, description="Username of the user")
