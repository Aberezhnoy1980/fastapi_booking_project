from pydantic import BaseModel, Field, ConfigDict


class RoomAddRequest(BaseModel):
    title: str = Field(description="Наименование номера")
    description: str | None = Field(None, description="Описание номера")
    price: int = Field(description="Стоимость проживания")
    quantity: int = Field(description="Количество доступных номеров")


class RoomAdd(BaseModel):
    hotel_id: int | None = Field(None, description="Идентификатор отеля")
    title: str = Field(description="Наименование номера")
    description: str | None = Field(None, description="Описание номера")
    price: int = Field(description="Стоимость проживания")
    quantity: int = Field(description="Количество доступных номеров")


class Room(RoomAdd):
    id: int = Field(description="Идентификатор номера")

    model_config = ConfigDict(from_attributes=True)


class RoomPatchRequest(BaseModel):
    title: str | None = Field(None, description="Наименование номера")
    description: str | None = Field(None, description="Описание номера")
    price: int | None = Field(None, description="Стоимость проживания")
    quantity: int | None = Field(None, description="Количество доступных номеров")


class RoomPatch(BaseModel):
    hotel_id: int | None = Field(None, description="Идентификатор отеля")
    title: str | None = Field(None, description="Наименование номера")
    description: str | None = Field(None, description="Описание номера")
    price: int | None = Field(None, description="Стоимость проживания")
    quantity: int | None = Field(None, description="Количество доступных номеров")
