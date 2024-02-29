from app.crud.token import get_user_by_token
from app.core.exceptions import DetailedHTTPException
from app.models.user import User

import hashlib

def hash_sha256(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()

def authorization_check(authorization) -> User:
    user = get_user_by_token(authorization)
    if user is None:
        raise DetailedHTTPException(401, 'Переданный токен не существует либо некорректен')
    return user