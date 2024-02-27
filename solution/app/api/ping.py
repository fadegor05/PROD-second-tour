from typing import Dict

from app.api.api_router import api_router

@api_router.get('/ping')
def ping_handler() -> Dict[str, str]:
    return {'status': 'ok'}