from typing import Annotated
from fastapi import Header

from app.api.api_router import api_router
from app.core.utils import get_user_by_token
from app.schemas.post import PostBase
from app.crud.post import create_post, get_post_response_by_id
from app.schemas.post import PostOut

@api_router.post('/posts/new')
def post_new_post(post_schema: PostBase, authorization: Annotated[str, Header()]) -> PostOut:
    user = get_user_by_token(authorization)
    post = create_post(post_schema, user.login)
    post_response = get_post_response_by_id(post.id)
    return post_response