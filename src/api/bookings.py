from fastapi import APIRouter, Body, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.utils.openapi_examples import booking_examples

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get(
    "",
    summary="Получение всех бронирований",
    description="Возвращает список всех бронирований из базы данных")
async def get_bookings(
        db: DBDep
):
    return await db.bookings.get_all()


@router.get(
    "/me",
    summary="Получение бронирований текущего пользователя",
    description="Возвращает список бронирований отфильтрованных по идентификатору пользователя"
)
async def get_user_bookings(
        db: DBDep,
        user_id: UserIdDep
):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post(
    "",
    summary="Добавление бронирования",
    description="<h2>Добавляет данные о бронировании в базу данных</h2>"
)
async def create_booking(
        db: DBDep,
        user_id: UserIdDep,
        booking_data: BookingAddRequest = Body(openapi_examples=booking_examples)
):
    try:
        room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=f"Room with id {booking_data.room_id} not found") from e

    room_price: int = room.price
    _booking_data = BookingAdd(user_id=user_id, price=room_price, **booking_data.model_dump())

    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}
