from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import SQLALCHEMY_DB_URL
from sqlalchemy import create_engine

engine = create_engine(SQLALCHEMY_DB_URL)