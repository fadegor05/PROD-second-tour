from typing import TYPE_CHECKING, List
from uuid import uuid4
import datetime

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, func, DateTime
from app.db.base import Base

if TYPE_CHECKING:
    from .user import User
    from .review import Review
    from .tag import Tag

class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(unique=True, default=str(uuid4()))
    content: Mapped[str]
    author: Mapped['User'] = relationship(back_populates='posts')
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    tags: Mapped[List['Tag']] = relationship(back_populates='post')
    createdAt: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
    )
    reviews: Mapped[List['Review']] = relationship(back_populates='post')
    

