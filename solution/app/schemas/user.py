import re, string
from pydantic import BaseModel, validator

class UserBase(BaseModel):
    login: str
    email: str
    password: str
    countryCode: str
    isPublic: bool
    phone: str
    image: str

    @validator('login')
    def validate_login(cls, value) -> str | None:
        if re.match(r'^[a-zA-Z0-9-]+$', value) and len(value) <= 30:
            return value
        
    @validator('email')
    def validate_email(cls, value) -> str | None:
        if len(value) <= 50:
            return value

    @validator('password')
    def validate_password(cls, value) -> str | None:
        if re.findall(r'[a-z]', value) and re.findall(r'[A-Z]', value) and re.findall(r'[0-9]', value) and len(value) >= 6 and len(value) <= 100:
            return value
        
    @validator('countryCode')
    def validate_country_code(cls, value) -> str | None:
        if re.match(r'^[a-zA-Z]{2}$', value) and len(value) <= 2:
            return value

    @validator('phone')
    def validate_phone(cls, value) -> str | None:
        if re.match(r'^\+[\d]+$', value):
            return value

    @validator('image')
    def validate_image(cls, value) -> str | None:
        if len(value) <= 200:
            return value