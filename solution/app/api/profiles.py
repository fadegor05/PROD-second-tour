from typing import Annotated
from fastapi import Path, Header

from app.api.api_router import api_router
from app.core.utils import authorization_check
from app.crud.user import get_user_by_login
from app.crud.friends import is_user_followed_on_user_by_login
from app.core.exceptions import DetailedHTTPException
from app.schemas.user import UserDB

@api_router.get('/profiles/{login}', response_model_exclude_none=True)
def get_profile_by_login_handler(login: Annotated[str, Path()], authorization: Annotated[str, Header()]) -> UserDB:
    user = authorization_check(authorization)
    user_profile = get_user_by_login(login)
    if user_profile is None:
        raise DetailedHTTPException(403, 'Пользователь с данным логином не существует')
    
    if not is_user_followed_on_user_by_login(user.login, user_profile.login) and not user_profile.isPublic:
        raise DetailedHTTPException(403, 'Нет доступа к запрашиваемому профилю')
    
    user_response = UserDB.model_validate(user_profile, from_attributes=True)
    return user_response