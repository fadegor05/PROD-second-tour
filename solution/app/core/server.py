from typing import Tuple
from fastapi import FastAPI, APIRouter
from app.core.routers import routers
from app.core.exceptions import HTTPExceptionPydantic, http_exception_pydantic_handler

class Server:

    app: FastAPI


    def __init__(self, app: FastAPI) -> None:
        self.app = app
        self.register_routers(routers)
        self.register_exception_handler(HTTPExceptionPydantic, http_exception_pydantic_handler)


    def get_app(self) -> FastAPI:
        return self.app
    
    def register_routers(self, routers: Tuple[APIRouter]):
        for router in routers:
            self.app.include_router(router = router)

    def register_exception_handler(self, handler, exception_handler):
        self.app.add_exception_handler(handler, exception_handler)