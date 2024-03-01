from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, func, DateTime
from app.db.base import Base

if TYPE_CHECKING:
    from .user import User
    from .post import Post

class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='reviews')

    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    post: Mapped['Post'] = relationship(back_populates='reviews')

    vote: Mapped[bool]

