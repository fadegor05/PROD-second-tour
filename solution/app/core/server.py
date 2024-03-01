from typing import Tuple
from fastapi import FastAPI, APIRouter, status, Request
from app.schemas.error import ErrorSchema
from app.core.routers import routers
from app.core.exceptions import DetailedHTTPException, detailed_http_exception_handler, validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

class Server:

    app: FastAPI


    def __init__(self, app: FastAPI) -> None:
        self.app = app
        self.register_routers(routers)
        self.register_exception_handler(DetailedHTTPException, detailed_http_exception_handler)
        self.register_exception_handler(RequestValidationError, validation_exception_handler)


    def get_app(self) -> FastAPI:
        return self.app
    
    def register_routers(self, routers: Tuple[APIRouter]):
        for router in routers:
            self.app.include_router(router = router)

    def register_exception_handler(self, handler, exception_handler):
        self.app.add_exception_handler(handler, exception_handler)
    