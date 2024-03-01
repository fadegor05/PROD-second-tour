from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .token import Token
    from .friend import Friend
    from .review import Review

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str]
    email: Mapped[str]
    hashed_password: Mapped[str]
    countryCode: Mapped[str]
    isPublic: Mapped[bool]
    phone: Mapped[str | None] = mapped_column(default=None)
    image: Mapped[str | None] = mapped_column(default=None)
    tokens: Mapped[List['Token']] = relationship(back_populates='user')
    follows: Mapped[List['Friend']] = relationship('Friend', back_populates='follower', foreign_keys='Friend.follower_id')
    followers: Mapped[List['Friend']] = relationship('Friend', back_populates='followes', foreign_keys='Friend.followes_id')
    reviews: Mapped[List['Review']] = relationship(back_populates='user')