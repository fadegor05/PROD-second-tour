from typing import Annotated, Dict
from fastapi import Header, Query

from app.api.api_router import api_router
from app.core.utils import authorization_check
from app.core.exceptions import DetailedHTTPException
from app.crud.user import get_user_by_login
from app.schemas.user import UserLogin
from app.crud.friends import follow_by_login, unfollow_by_login, get_follows_by_login
from app.schemas.status import STATUS_OK

@api_router.post('/friends/add')
def post_friend_add_handler(user_schema: UserLogin, authorization: Annotated[str, Header()]) -> Dict:
    user = authorization_check(authorization)
    user_friend = get_user_by_login(user_schema.login)
    if user_friend is None:
        raise DetailedHTTPException(404, 'Пользователь с указанным логином не найден')
    follow_by_login(user.login, user_friend.login)
    return STATUS_OK

@api_router.post('/friends/remove')
def post_friend_remove_handler(user_schema: UserLogin, authorization: Annotated[str, Header()]) -> Dict:
    user = authorization_check(authorization)
    user_friend = get_user_by_login(user_schema.login)
    if user_friend is None:
        raise DetailedHTTPException(404, 'Пользователь с указанным логином не найден')
    unfollow_by_login(user.login, user_friend.login)
    return STATUS_OK

@api_router.get('/friends')
def get_friends_handler(limit: Annotated[int, Query()] = 5, offset: Annotated[int, Query()] = 0, authorization: Annotated[str, Header()] = None):
    user = authorization_check(authorization)
    follows = get_follows_by_login(user.login, limit, offset)
    return follows