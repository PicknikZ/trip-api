from collections.abc import Iterable

from fastapi import FastAPI
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import (
    validation_error_definition,
    validation_error_response_definition,
)
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import *

from app.utils.errors.exceptions import *
from app.utils.response.response import CommonResponse


def register_exception_handler(app: FastAPI):
    app.add_exception_handler(MysqlException, mysql_error_handler)
    app.add_exception_handler(ServerException, server_exception_handler)
    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler)


async def mysql_error_handler(request: Request, exc: MysqlException):
    return JSONResponse(
        {"errors": [exc.details], "db_name": exc.table_name, "action": exc.action}, status_code=HTTP_405_METHOD_NOT_ALLOWED
    )

async def server_exception_handler(request: Request, e: ServerException) -> JSONResponse:
    return CommonResponse.failed(status_code=e.status_code, err_msg=e.detail)

async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    try:
        return JSONResponse(
            {"errors": [exc.detail]}, status_code=exc.status_code, headers=exc.headers
        )
    except AttributeError:
        try:
            return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)
        except AttributeError:
            return JSONResponse({"errors": [exc.detail]})


async def http_422_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handler for 422 error to transform default pydantic error object to gothinkster format
    """

    errors = {"body": []}

    if isinstance(exc.detail, Iterable) and not isinstance(
        exc.detail, str
    ):  # check if error is pydantic's model error
        for error in exc.detail:
            error_name = ".".join(
                error["loc"][1:]
            )  # remove 'body' from path to invalid element
            errors["body"].append({error_name: error["msg"]})
    else:
        errors["body"].append(exc.detail)

    return JSONResponse({"errors": errors}, status_code=HTTP_422_UNPROCESSABLE_ENTITY)


validation_error_definition["properties"] = {
    "body": {"title": "Body", "type": "array", "items": {"type": "string"}}
}

validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": REF_PREFIX + "ValidationError"},
    }
}
