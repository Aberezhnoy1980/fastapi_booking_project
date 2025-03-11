from fastapi import APIRouter, Query, Body

from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH
from templates.openapi_examples import post_examples as post_exs
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получение данных по отелю",
    description="<h2>Возвращает данные по отелю или группе или всем</h2>"
)
async def get_hotel(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Адрес отеля")
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.post(
    "",
    summary="Добавление отеля",
    description="<h2>Добавляет запись об отеле</h2>"
)
async def create_hotel(hotel_data: Hotel = Body(openapi_examples=post_exs)):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.put(
    "/{id}",
    summary="Обновление данных об отеле",
    description="<h2>Обновляет данные об отеле. Требуются все параметры (поля/свойства сущности/модели)</h2>"
)
async def update_hotel(
        hotel_id: int,
        hotel_data: Hotel = Body()
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch(
    "/{id}",
    summary="Частичное обновление данных об отеле",
    description="<h2>Здесь мы частично обновляем данные для отеля</h2>"
)
async def partially_update_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH = Body()
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(
            hotel_data,
            exclude_unset=True,
            id=hotel_id
        )
        await session.commit()
    return {"status": "OK"}


@router.delete(
    "/{id}",
    summary="Удаление отеля",
    description="<h2>Удаляет запись об отеле из базы данных</h2>"
)
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return_message = {"status": "OK"}
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return return_message
