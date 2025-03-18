from fastapi import APIRouter, Body, Path, HTTPException
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.database import async_session_maker
from src.exceptions.exc import RoomNotFound
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPATCH
from templates.openapi_examples import room_examples

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get(
    "/{hotel_id}/rooms",
    summary="Получение данных по номерам отеля",
    description="<h2>Возвращает данные по номерам указанного отеля</h2>",
)
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(hotel_id)


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Получение номера конкретного отеля по указанному идентификатору",
    description="Возвращает номер по идентификатору")
async def get_room_by_id(room_id: int = Path()):
    async with async_session_maker() as session:
        try:
            return await RoomsRepository(session).get_data_by_id(room_id)
        except NoResultFound:
            raise HTTPException(status_code=404, detail=f"Номер с id {room_id} не найден")


@router.post(
    "/{hotel_id}/rooms",
    summary="Добавление номера",
    description="<h2>Добавляет данные о номере в базу данных</h2>",
)
async def create_room(hotel_id: int, room_data: RoomAdd = Body(openapi_examples=room_examples)):
    room_data.hotel_id = hotel_id
    async with async_session_maker() as session:
        try:
            room = await RoomsRepository(session).add(room_data)
        except IntegrityError as e:
            raise HTTPException(status_code=404, detail=f"Hotel with id {hotel_id} not found") from e
        await session.commit()
    return {"status": "OK", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Обновление данных о номере",
    description="<h2>Обновляет данные о номере</h2>"
)
async def update_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomAdd = Body()
):
    room_data.hotel_id = hotel_id
    async with async_session_maker() as session:
        try:
            await RoomsRepository(session).edit(room_data, id=room_id)
        except IntegrityError as e:
            raise HTTPException(status_code=403, detail=f"Hotel with id {hotel_id} not found") from e
        await session.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных о номере",
    description="<h2>Обновляет указанные данные о номере</h2>"
)
async def partially_update_hotel(
        hotel_id: int,
        room_id: int,
        room_data: RoomPATCH = Body()
):
    room_data.hotel_id = hotel_id
    async with async_session_maker() as session:
        try:
            await RoomsRepository(session).edit(room_data,
                                                exclude_unset=True,
                                                id=room_id)
        except IntegrityError as e:
            raise HTTPException(status_code=403, detail=f"Hotel with id {hotel_id} not found") from e
        await session.commit()
    return {"status": "OK"}


@router.delete(
    "/rooms/{room_id}",
    summary="Удаление номера",
    description="<h2>Удаляет запись о номере в базе данных</h2>"
)
async def delete_room(
        room_id: int = Path()
):
    async with async_session_maker() as session:
        try:
            await RoomsRepository(session).delete(id=room_id)
        except NoResultFound as e:
            raise HTTPException(status_code=403, detail=f"Room with id {room_id} not found") from e
        await session.commit()
        return {"status": f"Successfully deleted room with id {room_id}"}
