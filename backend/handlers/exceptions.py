from typing import Union

from fastapi import Request, responses
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import ValidationError
from sqlalchemy.exc import DBAPIError, IntegrityError


def validation_error_handler(
    request: Request, exec: ValidationError
) -> responses.JSONResponse:
    error = exec.errors()[0]
    field = error.get("loc")[-1]
    message = error.get("msg")

    error_msg = f"Invalid {field}: {message}"
    return responses.JSONResponse(status_code=422, content={"error": error_msg})


def value_error_handler(request: Request, exec: ValueError):
    error_msg = exec.args[0]
    return responses.JSONResponse(status_code=404, content={"error": error_msg})


def auth_error_handler(request: Request, exec: AuthJWTException):
    return responses.JSONResponse(status_code=403, content={"error": exec.message})


def db_error_handler(request: Request, exec: Union[IntegrityError, DBAPIError]):
    error_msg = exec.args[0]
    if "UNIQUE" in error_msg:
        error_msg = (
            f"{error_msg.split(':')[1].split('.')[1].capitalize()} already exist"
        )
    return responses.JSONResponse(status_code=422, content={"error": error_msg})
