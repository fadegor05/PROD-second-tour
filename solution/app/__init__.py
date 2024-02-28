from fastapi import FastAPI
from app.core.server import Server
from app.db.session import Session
from app.db.base import Base

def create_app(_=None) -> FastAPI:
    with Session.begin() as session:
        Base.metadata.create_all(session.bind)
    app = FastAPI()
    return Server(app).get_app()