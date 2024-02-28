from pydantic import BaseModel

class ErrorSchema(BaseModel):
    reason: str