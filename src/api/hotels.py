from fastapi import APIRouter, Query, Body

from sqlalchemy import insert, select

from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH
from templates.openapi_examples import post_examples as post_exs
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("",
            summary="Получение данных по отелю",
            description="<h2>Возвращает данные по отелю или группе или всем</h2>")
async def get_hotel(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Идентификатор отеля"),
        title: str | None = Query(None, description="Название отеля")
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if id:
            query = query.filter_by(id=id)
        if title:
            query = query.filter_by(title=title)
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        result = await session.execute(query)

        hotels_ = result.scalars().all()
        return hotels_


# body, request body
@router.post("",
             summary="Добавление отеля",
             description="<h2>Добавляет запись об отеле</h2>")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples=post_exs)):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}",
            summary="Обновление данных об отеле",
            description="<h2>Обновляет данные об отеле. Требуются все параметры (поля/свойства сущности/модели)</h2>")
def update_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.patch("/{hotel_id}",
              summary="Частичное обновление данных об отеле",
              description="<h2>Здесь мы частично обновляем данные для отеля</h2>")
def partially_update_hotel(hotel_id: int, hotel_data: HotelPATCH):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.delete("/{hotel_id}",
               summary="Удаление отеля",
               description="<h2>Удаляет запись об отеле из базы данных</h2>")
def delete_hotel(hotel_id: int):
    # for hotel in hotels:
    #     if hotel["id"] == hotel_id:
    #         hotels.remove(hotel)
    # hotels.remove({hotel for hotel in hotels if hotel["id"] == hotel_id}.pop())
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
