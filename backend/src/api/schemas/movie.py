from pydantic import BaseModel, ConfigDict, Field


class MovieCreate(BaseModel):
    title: str = Field(..., description="Title of the movie")
    poster_key: str = Field(..., description="Poster key of the movie")
    genre: str = Field(..., description="Genre of the movie")
    duration: int = Field(..., description="Duration of the movie in minutes")


class MovieResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="ID of the movie")
    title: str = Field(..., description="Title of the movie")
    poster_key: str = Field(..., description="Poster key of the movie")
    genre: str = Field(..., description="Genre of the movie")
    duration: int = Field(..., description="Duration of the movie in minutes")
