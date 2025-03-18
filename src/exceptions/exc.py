class NoResultFound(BaseException):
    pass


class HotelNotFound(NoResultFound):
    def __init__(self, hotel_id: int):
        self.hotel_id = hotel_id
        super().__init__(f"Hotel with id: {hotel_id} not found")


class RoomNotFound(NoResultFound):
    def __init__(self, room_id: int):
        self.room_id = room_id
        super().__init__(f"Room with id: {room_id} not found")
