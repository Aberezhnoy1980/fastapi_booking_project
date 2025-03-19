from fastapi import APIRouter, Query, Body, Path

from src.schemas.hotels import HotelPATCH, HotelAdd
from src.utils.openapi_examples import hotel_examples
from src.api.dependencies import PaginationDep, DBDep

from sqlalchemy.exc import MultipleResultsFound
from src.exceptions.exc import HotelNotFound

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получение данных по отелю",
    description="<h2>Возвращает данные по отелю или группе или всем</h2>"
)
async def get_hotel(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Адрес отеля")
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get("/{hotel_id}")
async def get_hotel_by_id(
        db: DBDep,
        hotel_id: int = Path()
):
    try:
        result = await db.hotels.get_data_by_id(data_id=hotel_id)
        if result is None:
            raise HotelNotFound(hotel_id)
        return result
    except MultipleResultsFound:
        print("Найдено несколько записей. Непонятно как такое могло выйти")
        raise
    except HotelNotFound:
        print("Отель не найден")
        raise


@router.post(
    "",
    summary="Добавление отеля",
    description="<h2>Добавляет запись об отеле</h2>"
)
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples=hotel_examples)
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="Обновление данных об отеле",
    description="<h2>Обновляет данные об отеле. Требуются все параметры (поля/свойства сущности/модели)</h2>"
)
async def update_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelAdd = Body()
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h2>Здесь мы частично обновляем данные для отеля</h2>"
)
async def partially_update_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelPATCH = Body()
):
    await db.hotels.edit(
        hotel_data,
        exclude_unset=True,
        id=hotel_id
    )
    await db.commit()
    return {"status": "OK"}


@router.delete(
    "/{hotel_id}",
    summary="Удаление отеля",
    description="<h2>Удаляет запись об отеле из базы данных</h2>"
)
async def delete_hotel(
        db: DBDep,
        hotel_id: int = Path()
):
    return_message = {"status": "OK"}
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return return_message
