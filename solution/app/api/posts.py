from typing import Annotated
from fastapi import Header, Path, Query

from app.api.api_router import api_router
from app.core.utils import get_user_by_token
from app.core.exceptions import DetailedHTTPException
from app.schemas.post import PostBase
from app.crud.post import create_post, get_post_response_by_id, get_post_by_uuid, get_feed_by_user_login
from app.crud.friends import is_followed_on_by_login
from app.crud.user import get_user_by_login
from app.schemas.post import PostOut

@api_router.post('/posts/new')
def post_new_post_handler(post_schema: PostBase, authorization: Annotated[str, Header()]) -> PostOut:
    user = get_user_by_token(authorization)
    post = create_post(post_schema, user.login)
    post_response = get_post_response_by_id(post.id)
    return post_response

@api_router.get('/posts/{postUuid}')
def get_post_by_uuid_handler(postUuid: Annotated[str, Path()], authorization: Annotated[str, Header()]):
    user = get_user_by_token(authorization)
    post = get_post_by_uuid(postUuid)
    if post is None:
        raise DetailedHTTPException(404, 'Запрашиваемый пост не найден')
    post_response = get_post_response_by_id(post.id)
    post_author = get_user_by_login(post_response.author)
    if not (is_followed_on_by_login(post_author.login, user.login) or post_author.isPublic) and user.login != post_author.login:
        raise DetailedHTTPException(404, 'Нет доступа к запрашиваемому посту')
    return post_response

@api_router.get('/posts/feed/{login}')
def get_feed_by_login_handler(login: Annotated[str, Path()], limit: Annotated[int, Query()] = 5, offset: Annotated[int, Query()] = 0, authorization: Annotated[str, Header()] = None):
    user = get_user_by_token(authorization)
    if login == 'my':
        login = user.login
    feed_user = get_user_by_login(login)
    if not (is_followed_on_by_login(login, user.login) or feed_user.isPublic) and user.login != login:
        raise DetailedHTTPException(404, 'Нет доступа к запрашиваемой ленте')
    feed = get_feed_by_user_login(login, offset, limit)
    return feed