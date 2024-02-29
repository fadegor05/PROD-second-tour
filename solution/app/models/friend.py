from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey

from app.db.base import Base

if TYPE_CHECKING:
    from .user import User

class Friend(Base):
    __tablename__ = 'friends'

    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    follower: Mapped['User'] = relationship(back_populates='follows', foreign_keys=[follower_id], overlaps='followers')

    followes_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    followes: Mapped['User'] = relationship(back_populates='followers', foreign_keys=[followes_id], overlaps='follows')

    
    