from typing import List
from sqlalchemy import select, desc

from app.schemas.post import PostBase, PostOut
from app.models.post import Post
from app.models.tag import Tag
from app.models.user import User
from app.db.session import Session


def get_feed_by_user_login(user_login: str, offset: int, limit: int) -> List[Post]:
    user_stmt = select(User).where(User.login == user_login)
    with Session() as session:
        user = session.execute(user_stmt).scalar_one_or_none()
        feed_stmt = select(Post).where(Post.author_id == user.id).order_by(desc(Post.createdAt))
        feed = session.execute(feed_stmt).scalars().all()
        posts = []
        for n, post in enumerate(feed):
            if n >= offset and len(posts) < limit:
                likes = 0
                dislikes = 0
                for review in post.reviews:
                    if review.vote:
                        likes += 1
                    else:
                        dislikes += 1
                post_out = PostOut(id=post.uuid,
                                   content=post.content,
                                   tags=[item.tag for item in post.tags],
                                   author=post.author.login,
                                   createdAt=post.createdAt.isoformat(),
                                   likesCount=likes,
                                   dislikesCount=dislikes)
                posts.append(post_out)
        return posts

def get_post_by_uuid(post_uuid: str) -> Post:
    stmt = select(Post).where(Post.uuid == post_uuid)
    with Session() as session:
        post = session.execute(stmt).scalar_one_or_none()
        return post

def get_post_response_by_id(post_id: int) -> PostOut:
    post_stmt = select(Post).where(Post.id == post_id)
    with Session() as session:
        post = session.execute(post_stmt).scalar_one_or_none()
        likes = 0
        dislikes = 0
        for review in post.reviews:
            if review.vote:
                likes += 1
            else:
                dislikes += 1

        post_out = PostOut(id=post.uuid,
                           content=post.content,
                           tags=[item.tag for item in post.tags],
                           author=post.author.login, 
                           createdAt=post.createdAt.isoformat(), 
                           likesCount=likes, 
                           dislikesCount=dislikes)
        return post_out

def create_post(post_schema: PostBase, user_login: str) -> Post:
    user_stmt = select(User).where(User.login == user_login)
    with Session() as session:
        user = session.execute(user_stmt).scalar_one_or_none()
        tags = []
        for tag in post_schema.tags:
            tags.append(Tag(tag=tag))
        post = Post(content=post_schema.content, tags=tags, author=user)
        session.add(post)
        session.commit()
        session.refresh(post)
        return post