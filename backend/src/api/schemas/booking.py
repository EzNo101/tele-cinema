from pydantic import BaseModel, ConfigDict, Field

from src.infra.db.models.booking import BookingStatus


class BookingCreate(BaseModel):
    user_id: int = Field(..., description="ID of the user")
    seat_id: int = Field(..., description="ID of the seat")


class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="ID of the booking")
    session_id: int = Field(..., description="ID of the movie session")
    user_id: int = Field(..., description="ID of the user")
    seat_id: int = Field(..., description="ID of the seat")
    price_stars: int = Field(..., description="Price of the booking in telegram stars")
    status: BookingStatus = Field(..., description="Status of the booking")


class BookingUpdateStatus(BaseModel):
    status: BookingStatus = Field(..., description="New status of the booking")
