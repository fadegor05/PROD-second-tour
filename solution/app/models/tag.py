from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from .post import Post

class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    post: Mapped['Post'] = relationship(back_populates='tags')
    tag: Mapped[str]