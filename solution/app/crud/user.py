from sqlalchemy import select, or_

from app.db.session import Session
from app.schemas.user import UserBase, UserDB
from app.models.user import User


def is_user_unique(login: str, email: str, phone: str | None = None) -> bool:
    stmt = select(User).where(or_(User.login == login, User.email == email, User.phone == phone))
    if phone is None:
        stmt = select(User).where(or_(User.login == login, User.email == email))
    with Session() as session:
        result = session.execute(stmt)
        return len(result.scalars().all()) == 0

def create_user(user_schema: UserDB) -> User | None:
    if not is_user_unique(user_schema.login, user_schema.email, user_schema.phone):
        return None
    user = User(login=user_schema.login,
                email=user_schema.email,
                password=user_schema.password,
                countryCode=user_schema.countryCode,
                isPublic=user_schema.isPublic,
                phone=user_schema.phone,
                image=user_schema.image)
    with Session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
