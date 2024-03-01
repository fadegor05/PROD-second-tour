from sqlalchemy import select

from app.schemas.post import PostBase, PostOut
from app.models.post import Post
from app.models.tag import Tag
from app.models.user import User
from app.db.session import Session


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