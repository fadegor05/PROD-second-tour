from datetime import datetime, timezone

from sqlalchemy import select, or_, and_

from app.models.token import Token
from app.models.user import User
from app.db.session import Session

from secrets import token_urlsafe

def delete_token(token: Token) -> None:
    with Session() as session:
        session.delete(token)
        session.commit()

def is_token_exist(token: Token) -> bool:
    current_datetime = datetime.now(timezone.utc)
    difference = current_datetime - token.created_at
    if difference.total_seconds() / 3600 >= 24:
        delete_token(token)
        return False
    return True

def get_user_by_token(token_str: str) -> User | None:
    stmt = select(Token).where(Token.token == token_str.replace('Bearer ', ''))
    with Session() as session:
        result = session.execute(stmt)
        token = result.scalar_one_or_none()
        if token is None:
            return None
        user = token.user
    return user if is_token_exist(token) else None

def create_token(user: User) -> Token | None:
    token = Token(token=token_urlsafe(64), user=user)
    with Session() as session:
        session.add(token)
        session.commit()
        session.refresh(token)
        return token