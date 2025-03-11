class HotelGettingException(Exception):
    pass


class HotelNotFound(HotelGettingException):
    def __init__(self):
        super().__init__("Hotel not found")
