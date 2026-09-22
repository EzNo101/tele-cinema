from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MovieSessionCreate(BaseModel):
    movie_id: int = Field(..., description="ID of the movie")
    room_id: int = Field(..., description="ID of the room")
    start_time: datetime = Field(
        ...,
        description="Start time of the movie session in ISO 8601 format",
    )
    price_stars: int = Field(
        ...,
        description="Price of the movie session in telegram stars",
    )


class MovieSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="ID of the movie session")
    movie_id: int = Field(..., description="ID of the movie")
    room_id: int = Field(..., description="ID of the room")
    start_time: datetime = Field(
        ...,
        description="Start time of the movie session in ISO 8601 format",
    )
    price_stars: int = Field(
        ...,
        description="Price of the movie session in telegram stars",
    )
