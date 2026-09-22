from pydantic import BaseModel, ConfigDict, Field


class RoomCreate(BaseModel):
    name: str = Field(..., description="Name of the room")
    rows: int = Field(..., description="Number of rows in the room")
    columns: int = Field(..., description="Number of columns in the room")


class RoomResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="ID of the room")
    name: str = Field(..., description="Name of the room")
    rows: int = Field(..., description="Number of rows in the room")
    columns: int = Field(..., description="Number of columns in the room")
