from typing import Annotated

from fastapi import Header

from app.api.api_router import api_router
from app.crud.token import get_user_by_token
from app.crud.user import update_user, update_user_password, delete_all_user_tokens
from app.core.exceptions import DetailedHTTPException
from app.schemas.user import UserDB, UserDBUpdate, UserPasswordUpdate
from app.core.utils import authorization_check

@api_router.get('/me/profile', response_model_exclude_none=True)
def get_profile_handler(authorization: Annotated[str, Header()]) -> UserDB:
    user = authorization_check(authorization)
    user_response = UserDB.model_validate(user, from_attributes=True)
    return user_response

@api_router.patch('/me/profile', response_model_exclude_none=True)
def patch_profile_handler(user_schema: UserDBUpdate, authorization: Annotated[str, Header()]) -> UserDB:
    user = authorization_check(authorization)
    updated_user = update_user(user, user_schema)
    if updated_user is None:
        raise DetailedHTTPException(409, 'Такой e-mail, номер телефона или логин уже занят')
    user_response = UserDB.model_validate(updated_user, from_attributes=True)
    return user_response

@api_router.post('/me/updatePassword')
def post_update_password_handler(user_schema: UserPasswordUpdate, authorization: Annotated[str, Header()]):
    user = authorization_check(authorization)
    if not update_user_password(user, user_schema):
        raise DetailedHTTPException(403, 'Указанный пароль не совпадает с действительным')

    delete_all_user_tokens(user)

    return {'status': 'ok'}
