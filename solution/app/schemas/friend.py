from pydantic import BaseModel

class FriendBase(BaseModel):
    login: str
    addedAt: str