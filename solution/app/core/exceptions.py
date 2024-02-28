from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Request

class HTTPExceptionPydantic(HTTPException):
    pass


def http_exception_pydantic_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content=exc.detail.model_dump())