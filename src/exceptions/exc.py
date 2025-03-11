class HotelGettingException(Exception):
    pass


class HotelNotFound(HotelGettingException):
    def __init__(self, hotel_id: int):
        self.hotel_id = hotel_id
        super().__init__(f"Hotel with id: {hotel_id} not found")
