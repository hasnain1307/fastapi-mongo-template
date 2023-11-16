from starlette.exceptions import HTTPException


class UniqueKeyViolationException(HTTPException):
    """Exception raised when the unique key constraint is violated"""

    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class ObjectNotFoundException(HTTPException):
    """Exception raised when the object is not found"""

    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)
