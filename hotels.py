from fastapi import APIRouter, Query, Body

from schemas.hotels import Hotel, HotelPATCH
from templates.openapi_examples import post_examples as post_exs

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"}
]


@router.get("",
            summary="Получение данных по отелю",
            description="<h2>Возвращает данные по отелю или группе или всем</h2>")
def get_hotel(
        id: int | None = Query(None, description="Идентификатор отеля"),
        title: str | None = Query(None, description="Название отеля"),
        page: int | None = Query(1, description="Номер страницы"),
        per_page: int | None = Query(3, description="Количество записей на странице")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_[0:per_page]


# body, request body
@router.post("",
             summary="Добавление отеля",
             description="<h2>Добавляет запись об отеле</h2>")
def create_hotel(hotel_data: Hotel = Body(openapi_examples=post_exs)):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
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
