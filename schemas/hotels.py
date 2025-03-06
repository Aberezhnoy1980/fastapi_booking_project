from pydantic import BaseModel, Field


class Hotel(BaseModel):
    # hotel_id: int = Path(description="Идентификатор отеля")
    title: str = Field(description="Название отеля")
    name: str = Field(description="Название курорта")


class HotelPATCH(BaseModel):
    title: str | None = Field(None, description="Название отеля")
    name: str | None = Field(None, description="Название курорта")
