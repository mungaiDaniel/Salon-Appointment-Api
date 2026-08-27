class HttpError(Exception):
    """Bad Request"""

    error_code = "Bad Request"
    status_code = 400


class DatabaseError(HttpError):
    error_code = "Database Error"
    status_code = 500


class AuthenticationError(Exception):
    """Raised when authentication fails (bad credentials, missing user, etc.)."""

    def __init__(self, http_code: int, message: str, code: str = "test_stat"):
        super().__init__(message)
        self.http_code = http_code
        self.message = message
        self.code = code

