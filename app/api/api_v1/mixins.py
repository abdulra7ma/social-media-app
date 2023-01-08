from fastapi import HTTPException
from app.db_models.post import PostModel
from app.db_models.user import UserModel


class PostAuthorizeMixin:
    @staticmethod
    def auth(post: PostModel, user: UserModel):
        if not post.user_id == user.id:
            raise HTTPException(status_code=403, detail="Unauthorized action")
