from app.api.api_router import api_router
from app.schemas.user import UserBase
from app.core.exceptions import DetailedHTTPException

AUTH_TROUBLES = {
    'login': 'Длина логина не более 30 символов, и содержит только a-z, A-Z, 0-9',
    'email': 'Длина емейла не более 50 символов',
    'password': 'Длина паsoроля не менее 6, но и не более 100 символов, содержит только a-z A-Z, присутствует минимум одна цифра',
    'countryCode': 'Страна с указанным кодом не найдена',
    'phone': 'Номер начинается с + и после содержит только цифры 0-9',
    'image': 'Длина ссылки на аватар пользователя превышает допустимый лимит'
}

@api_router.post('/auth/register')
def register_user_handler(user: UserBase):
    user_dict = user.model_dump()
    for key in user_dict:
        if user_dict[key] is None:
            raise DetailedHTTPException(400, AUTH_TROUBLES[key])