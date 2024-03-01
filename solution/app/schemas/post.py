from typing import List
from pydantic import BaseModel, validator
from app.core.exceptions import DetailedHTTPException

class PostBase(BaseModel):
    content: str
    tags: List[str]

    @validator('content')
    def validate_content(cls, value):
        if len(value) <= 1000:
            return value
        
    @validator('tags')
    def validate_tags(cls, value):
        for tag in value:
            if not tag <= 20:
                raise DetailedHTTPException(400, 'Максимальная длина тега 20 символов')
        return value
    
class PostOut(PostBase):
    id: str
    author: str
    createdAt: str
    likesCount: int
    dislikesCount: int
    
