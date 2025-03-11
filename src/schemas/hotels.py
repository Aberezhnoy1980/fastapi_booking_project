from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str = Field(description="Название отеля")
    location: str = Field(description="Название курорта")


class HotelPATCH(BaseModel):
    title: str | None = Field(None, description="Название отеля")
    location: str | None = Field(None, description="Название курорта")


class HotelDELETE(BaseModel):
    id: int | None = Field(None, description="Идентификатор отеля")
    title: str | None = Field(None, description="Название отеля")
    location: str | None = Field(None, description="Название курорта")
