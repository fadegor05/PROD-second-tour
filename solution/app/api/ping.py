from typing import Dict

from app.schemas.status import STATUS_OK
from app.api.api_router import api_router

@api_router.get('/ping')
def ping_handler() -> Dict[str, str]:
    return STATUS_OK