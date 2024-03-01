from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request, status
from app.schemas.error import ErrorSchema

class DetailedHTTPException(HTTPException):
    pass

def detailed_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content=ErrorSchema(reason=exc.detail).model_dump())

def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=ErrorSchema(reason='Формат входного запроса не соответствует формату').model_dump())