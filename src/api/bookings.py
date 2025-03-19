from fastapi import APIRouter, Body, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.utils.openapi_examples import booking_examples

router = APIRouter(prefix="/booking", tags=["Бронирования"])


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

    _price = room.model_dump()["price"]
    _booking_data = BookingAdd(user_id=user_id, price=_price, **booking_data.model_dump())

    booking = await db.bookings.add(_booking_data)

    await db.commit()
    return {"status": "OK", "data": booking}
