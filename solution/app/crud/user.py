from sqlalchemy import select, or_, and_

from app.core.utils import hash_sha256
from app.db.session import Session
from app.schemas.user import UserDB, UserBase, UserDBUpdate
from app.models.user import User


def is_user_unique(login: str | None = None, email: str | None = None, phone: str | None = None) -> bool:
    filters = []
    if login is not None:
        filters.append(User.login == login)
    if email is not None:
        filters.append(User.email == email)
    if phone is not None:
        filters.append(User.phone == phone)
    
    if not filters:
        return False
    
    stmt = select(User).where(or_(*filters))

    with Session() as session:
        result = session.execute(stmt)
        return len(result.scalars().all()) == 0

def get_user_by_base(user_schema: UserBase) -> User | None:
    stmt = select(User).where(and_(User.login == user_schema.login, User.hashed_password == hash_sha256(user_schema.password)))
    with Session() as session:
        result = session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

def update_user(old_user: User, user_schema: UserDBUpdate) -> User | None:
    if not is_user_unique(user_schema.login, user_schema.email, user_schema.phone):
        return None
    stmt = select(User).where(User.login == old_user.login)
    update_user_dict = user_schema.model_dump(exclude_none=True)
    with Session() as session:
        result = session.execute(stmt)
        user = result.scalar_one_or_none()
        for key in update_user_dict:
            setattr(user, key, update_user_dict[key])
        session.commit()
        session.refresh(user)
        return user

def create_user(user_schema: UserDB) -> User | None:
    if not is_user_unique(user_schema.login, user_schema.email, user_schema.phone):
        return None
    user = User(**user_schema.model_dump(), hashed_password=hash_sha256(user_schema.password))
    with Session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    

