from pydantic import BaseModel, validator

class TokenBase(BaseModel):
    token: str

    @validator('token')
    def validate_token(cls, value):
        if len(value) >= 20:
            return value
        raise ValueError()