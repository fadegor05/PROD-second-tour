from app.models.token import Token
from app.models.user import User
from app.db.session import Session

from secrets import token_urlsafe

def create_token(user: User) -> Token | None:
    token = Token(token=token_urlsafe(64), user=user)
    with Session() as session:
        session.add(token)
        session.commit()
        session.refresh(token)
        return token