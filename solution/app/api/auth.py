from fastapi import Response, status

from app.api.api_router import api_router
from app.schemas.user import UserModel, UserDB, UserBase, UserToken
from app.core.exceptions import DetailedHTTPException
from app.crud.user import create_user
from app.crud.country import get_country_by_alpha2



@api_router.post('/auth/register', response_model_exclude_none=True)
def register_user_handler(user_schema: UserDB, response: Response) -> UserModel:
    if get_country_by_alpha2(user_schema.countryCode) is None:
        raise DetailedHTTPException(400, 'Страна с указанным кодом не найдена')
    user = create_user(user_schema)
    if user is None:
        raise DetailedHTTPException(409, 'Пользователь с таким e-mail, номером телефона или логином уже зарегистрирован')
    response.status_code = status.HTTP_201_CREATED
    user_response = UserModel(profile=UserDB.model_validate(user, from_attributes=True))
    return user_response

@api_router.post('/auth/sign-in')
def sign_in_user_handler(user_schema: UserBase, response: Response) -> UserToken:
    return UserToken(token='exampletokenexampletokenexampletokenexampletokenexampletokenexampletoken')