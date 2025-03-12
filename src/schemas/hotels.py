from pydantic import BaseModel, Field, ConfigDict


class HotelAdd(BaseModel):
    title: str = Field(description="Название отеля")
    location: str = Field(description="Название курорта")


class Hotel(HotelAdd):
    id: int = Field(description="Идентификатор отеля")

    model_config = ConfigDict(from_attributes=True)


class HotelPATCH(BaseModel):
    title: str | None = Field(None, description="Название отеля")
    location: str | None = Field(None, description="Название курорта")
