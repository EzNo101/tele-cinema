class UserNotFoundException(Exception):
    """Exception raised when a user is not found in the database."""


class UserAlreadyExistsException(Exception):
    """Exception raised when a user already exists in the database."""


class RoomNotFoundException(Exception):
    """Exception raised when a room is not found in the database."""


class RoomAlreadyExistsException(Exception):
    """Exception raised when a room already exists in the database."""


class MovieNotFoundException(Exception):
    """Exception raised when a movie is not found in the database."""


class MovieAlreadyExistsException(Exception):
    """Exception raised when a movie already exists in the database."""


class MovieSessionNotFoundException(Exception):
    """Exception raised when a movie session is not found in the database."""


class MovieSessionAlreadyExistsException(Exception):
    """Exception raised when a movie session already exists in the database."""


class SeatNotFoundException(Exception):
    """Exception raised when a seat is not found in the database."""


class SeatAlreadyExistsException(Exception):
    """Exception raised when a seat is already exists in the database."""


class BookingNotFoundException(Exception):
    """Exception raised when a booking is not found in the database."""


class BookingAlreadyExistsException(Exception):
    """Exception raised when a booking is already exists in the database."""
