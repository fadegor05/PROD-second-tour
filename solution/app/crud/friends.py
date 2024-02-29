from sqlalchemy import select, and_

from app.db.session import Session
from app.models.user import User
from app.models.friend import Friend


def is_user_followed_on_user_by_login(user_login: str, followes_login: str) -> bool:
    user_stmt = select(User).where(User.login == user_login)
    followes_stmt = select(User).where(User.login == followes_login)
    with Session() as session:
        follower_user = session.execute(user_stmt).scalar_one_or_none()
        followes_user = session.execute(followes_stmt).scalar_one_or_none()
        stmt = select(Friend).where(and_(Friend.follower_id == follower_user.id, Friend.followes_id == followes_user.id))
        friend = session.execute(stmt).scalar_one_or_none()
        return friend is not None

def add_follow_by_login(user_login: str, follower_login: str) -> None:
    if is_user_followed_on_user_by_login(user_login, follower_login):
        return
    user_stmt = select(User).where(User.login == user_login)
    follower_stmt = select(User).where(User.login == follower_login)
    with Session() as session:
        user = session.execute(user_stmt).scalar_one_or_none()
        follower_user = session.execute(follower_stmt).scalar_one_or_none()
        friend = Friend(follower=follower_user, followes=user)
        session.add(friend)
        session.commit()

def remove_follow_by_login(user_login: str, follower_login: str) -> None:
    if not is_user_followed_on_user_by_login(user_login, follower_login):
        return
    user_stmt = select(User).where(User.login == user_login)
    follower_stmt = select(User).where(User.login == follower_login)
    with Session() as session:
        user = session.execute(user_stmt).scalar_one_or_none()
        follower_user = session.execute(follower_stmt).scalar_one_or_none()
        stmt = select(Friend).where(and_(Friend.follower_id == follower_user.id, Friend.followes_id == user.id))
        friend = session.execute(stmt).scalar_one_or_none()
        session.delete(friend)
        session.commit()