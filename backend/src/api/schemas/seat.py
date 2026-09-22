from pydantic import BaseModel, ConfigDict, Field


class SeatCreate(BaseModel):
    session_id: int = Field(..., description="ID of the movie session")
    row: int = Field(..., description="Row number of the seat")
    number: int = Field(..., description="Seat number in the row")


class SeatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="ID of the seat")
    session_id: int = Field(..., description="ID of the movie session")
    row: int = Field(..., description="Row number of the seat")
    number: int = Field(..., description="Seat number in the row")
