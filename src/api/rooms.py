from fastapi import APIRouter, Body, Path, HTTPException
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest
from templates.openapi_examples import room_examples

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get(
    "/{hotel_id}/rooms",
    summary="Получение данных по номерам отеля",
    description="<h2>Возвращает данные по номерам указанного отеля</h2>",
)
async def get_rooms(
        db: DBDep,
        hotel_id: int = Path()
):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Получение номера конкретного отеля по указанному идентификатору",
    description="Возвращает номер по идентификатору")
async def get_room_by_id(
        db: DBDep,
        hotel_id: int = Path(),
        room_id: int = Path()
):
    try:
        return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Номер с id {room_id} не найден")


@router.post(
    "/{hotel_id}/rooms",
    summary="Добавление номера",
    description="<h2>Добавляет данные о номере в базу данных</h2>",
)
async def create_room(
        db: DBDep,
        hotel_id: int = Path(),
        room_data: RoomAddRequest = Body(openapi_examples=room_examples)
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

    try:
        room = await db.rooms.add(_room_data)
    except IntegrityError as e:
        raise HTTPException(status_code=404, detail=f"Hotel with id {hotel_id} not found") from e

    await db.commit()
    return {"status": "OK", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Обновление данных о номере",
    description="<h2>Обновляет данные о номере</h2>"
)
async def update_room(
        db: DBDep,
        hotel_id: int = Path(),
        room_id: int = Path(),
        room_data: RoomAddRequest = Body()
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

    try:
        await db.rooms.edit(_room_data, id=room_id)
    except IntegrityError as e:
        raise HTTPException(status_code=403, detail=f"Hotel with id {hotel_id} not found") from e

    await db.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных о номере",
    description="<h2>Обновляет указанные данные о номере</h2>"
)
async def partially_update_room(
        db: DBDep,
        hotel_id: int = Path(),
        room_id: int = Path(),
        room_data: RoomPatchRequest = Body()
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))

    try:
        await db.rooms.edit(_room_data,
                            exclude_unset=True,
                            id=room_id,
                            hotel_id=hotel_id)
    except IntegrityError as e:
        raise HTTPException(status_code=403, detail=f"Hotel with id {hotel_id} not found") from e

    await db.commit()
    return {"status": "OK"}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удаление номера",
    description="<h2>Удаляет запись о номере в базе данных</h2>"
)
async def delete_room(
        db: DBDep,
        hotel_id: int = Path(),
        room_id: int = Path()
):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": f"Successfully deleted room with id {room_id}"}
