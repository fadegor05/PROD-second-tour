from typing import Annotated

from fastapi import Header

from app.api.api_router import api_router
from app.crud.token import get_user_by_token
from app.core.exceptions import DetailedHTTPException
from app.schemas.user import UserDB

@api_router.get('/me/profile', response_model_exclude_none=True)
def get_profile_handler(authorization: Annotated[str, Header()]) -> UserDB:
    user = get_user_by_token(authorization)
    if user is None:
        raise DetailedHTTPException(401, 'Переданный токен не существует либо некорректен')
    
    user_response = UserDB.model_validate(user, from_attributes=True)
    return user_response