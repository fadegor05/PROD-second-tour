from typing import List
from sqlalchemy import select, and_

from app.db.session import Session
from app.models.user import User
from app.models.friend import Friend
from app.schemas.friend import FriendBase

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

#TODO
def get_follows_by_login(user_login: str) -> List[FriendBase]:
    user_stmt = select(User).where(User.login == user_login)
    with Session() as session:
        user = session.execute(user_stmt).scalar_one_or_none()
        follows_list = []
        for friend in user.follows:
            follows_list.append(FriendBase(login=friend.followes.login, addedAt=friend.addedAt.isoformat()))
        return follows_list