import pydantic


class UserNotFound(pydantic.BaseModel):
    """User Not Found Schema
    Attributes:
        error (str): error for the payload
    """

    error: str
    status_code: int = 404
