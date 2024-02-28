from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str]
    email: Mapped[str]
    countryCode: Mapped[str]
    isPublic: Mapped[bool]
    phone: Mapped[str]
    image: Mapped[str]