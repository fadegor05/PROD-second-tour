from fastapi import FastAPI
from app.core.server import Server
from app.db.session import Session
from app.db.base import Base

def create_app(_=None) -> FastAPI:
    with Session.begin():
        Base.metadata.create_all
    app = FastAPI()
    return Server(app).get_app()