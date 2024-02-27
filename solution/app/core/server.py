from typing import Tuple
from fastapi import FastAPI, APIRouter
from app.core.routers import routers

class Server:

    app: FastAPI


    def __init__(self, app: FastAPI) -> None:
        self.app = app
        self.register_routers(routers)


    def get_app(self) -> FastAPI:
        return self.app
    
    def register_routers(self, routers: Tuple[APIRouter]):
        for router in routers:
            self.app.include_router(router = router)