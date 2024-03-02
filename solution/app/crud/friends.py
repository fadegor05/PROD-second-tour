from typing import List
from sqlalchemy import select, and_, desc

from app.db.session import Session
from app.models.user import User
from app.models.friend import Friend
from app.schemas.friend import FriendBase

def can_user_access_user_by_login(user_login: str, target_login: str):
    user_stmt = select(User).where(User.login == user_login)
    target_stmt = select(User).where(User.login == target_login)
    with Session() as session:
        user = session.execute(user_stmt).scalar_one_or_none()
        target = session.execute(target_stmt).scalar_one_or_none()
        return is_followed_on_by_login(target.login, user.login) or target.isPublic or user.login == target.login

def is_followed_on_by_login(user_login: str, target_login: str) -> bool:
    user_stmt = select(User).where(User.login == user_login)
    target_stmt = select(User).where(User.login == target_login)
    with Session() as session:
        user = session.execute(user_stmt).scalar_one_or_none()
        target = session.execute(target_stmt).scalar_one_or_none()
        stmt = select(Friend).where(and_(Friend.follower_id == user.id, Friend.followes_id == target.id))
        friend = session.execute(stmt).scalar_one_or_none()
        return friend is not None

def follow_by_login(user_login: str, target_login: str) -> None:
    if is_followed_on_by_login(user_login, target_login):
        return None
    user_stmt = select(User).where(User.login == user_login)
    target_stmt = select(User).where(User.login == target_login)
    with Session() as session:
        user = session.execute(user_stmt).scalar_one_or_none()
        target = session.execute(target_stmt).scalar_one_or_none()
        friend = Friend(follower=user, followes=target)
        session.add(friend)
        session.commit()
        return None

def unfollow_by_login(user_login: str, target_login: str) -> None:
    if not is_followed_on_by_login(user_login, target_login):
        return None
    user_stmt = select(User).where(User.login == user_login)
    target_stmt = select(User).where(User.login == target_login)
    with Session() as session:
        user = session.execute(user_stmt).scalar_one_or_none()
        target = session.execute(target_stmt).scalar_one_or_none()
        stmt = select(Friend).where(and_(Friend.follower_id == user.id, Friend.followes_id == target.id))
        friend = session.execute(stmt).scalar_one_or_none()
        session.delete(friend)
        session.commit()
        return None

def get_follows_by_login(user_login: str, limit: int, offset: int) -> List[FriendBase]:
    user_stmt = select(User).where(User.login == user_login)
    with Session() as session:
        user = session.execute(user_stmt).scalar_one_or_none()
        follows_stmt = select(Friend).where(Friend.follower_id == user.id).order_by(desc(Friend.addedAt))
        friends = session.execute(follows_stmt).scalars().all()
        follows_list = []
        for n, friend in enumerate(friends):
            if n >= offset and len(follows_list) < limit:
                follows_list.append(FriendBase(login=friend.followes.login, addedAt=friend.addedAt.isoformat()))
        return follows_list