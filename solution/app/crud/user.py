from sqlalchemy import select, or_, and_

from app.db.session import Session
from app.schemas.user import UserDB, UserBase
from app.models.user import User


def is_user_unique(login: str, email: str, phone: str | None = None) -> bool:
    stmt = select(User).where(or_(User.login == login, User.email == email, User.phone == phone))
    if phone is None:
        stmt = select(User).where(or_(User.login == login, User.email == email))
    with Session() as session:
        result = session.execute(stmt)
        return len(result.scalars().all()) == 0

def validate_user_by_base(login: str, password: str) -> bool:
    stmt = select(User).where(and_(User.login == login, User.password == password))
    with Session() as session:
        result = session.execute(stmt)
        user = result.scalar_one_or_none()
        return user is not None

def create_user(user_schema: UserDB) -> User | None:
    if not is_user_unique(user_schema.login, user_schema.email, user_schema.phone):
        return None
    user = User(**user_schema.model_dump(), password=user_schema.password)
    with Session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    

