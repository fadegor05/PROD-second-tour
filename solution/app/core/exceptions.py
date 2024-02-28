from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Request
from app.schemas.error import ErrorSchema

class DetailedHTTPException(HTTPException):
    pass

def detailed_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content=ErrorSchema(reason=exc.detail).model_dump())