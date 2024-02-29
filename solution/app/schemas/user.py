from pydantic import BaseModel, Field, validator
from app.core.exceptions import DetailedHTTPException
import re



class UserBase(BaseModel):
    login: str
    password: str | None = Field(exclude=True)

    @validator('login')
    def validate_login(cls, value) -> str:
        if re.match(r'^[a-zA-Z0-9-]+$', value) and len(value) <= 30:
            return value
        raise DetailedHTTPException(400, 'Длина логина не более 30 символов, и содержит только a-z, A-Z, 0-9')

    @validator('password')
    def validate_password(cls, value) -> str:
        if re.findall(r'[a-z]', value) and re.findall(r'[A-Z]', value) and re.findall(r'[0-9]', value) and len(value) >= 6 and len(value) <= 100:
            return value
        raise DetailedHTTPException(400, 'Длина пароля не менее 6, но и не более 100 символов, содержит только a-z A-Z, присутствует минимум одна цифра')


class UserDB(UserBase):
    email: str
    countryCode: str
    isPublic: bool
    phone: str | None = None
    image: str | None = None
    password: str | None = Field(None, exclude=True)
        
    @validator('email')
    def validate_email(cls, value) -> str:
        if len(value) <= 50:
            return value
        raise DetailedHTTPException(400, 'Длина e-mail не более 50 символов')
        
    @validator('countryCode')
    def validate_country_code(cls, value) -> str:
        if re.match(r'^[a-zA-Z]{2}$', value) and len(value) <= 2:
            return value
        raise DetailedHTTPException(400, 'Длина кода страны 2 символа, и содержит только a-z, A-Z')

    @validator('phone')
    def validate_phone(cls, value) -> str | None:
        if value is None or (re.match(r'^\+[\d]+$', value) and len(value) <= 20):
            return value
        raise DetailedHTTPException(400, 'Номер начинается с + и после содержит только цифры 0-9')

    @validator('image')
    def validate_image(cls, value) -> str | None:
        if value is None or len(value) <= 200:
            return value
        raise DetailedHTTPException(400, 'Длина ссылки на аватар пользователя превышает допустимый лимит')

class UserDBUpdate(UserDB):
    login: str | None = None
    email: str | None = None
    countryCode: str | None = None
    isPublic: bool | None = None
    phone: str | None = None
    image: str | None = None

class UserModel(BaseModel):
    profile: UserDB