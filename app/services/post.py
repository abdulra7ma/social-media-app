from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker

from app.api.api_v1.mixins import PostAuthorizeMixin
from app.db.session import get_session
from app.db.redis import RedisConnection
from app.db_models.post import PostModel, LikeModel, DislikeModel
from app.db_models.user import UserModel
from app.models.post import PostIn, Post, PostInUpdate, ResponseGetPost

# from app.main import redis
redis = RedisConnection()


class BaseService:
    def __init__(self, session: sessionmaker = Depends(get_session)):
        self.async_session = session


class GetPostService(BaseService):
    async def execute(self, post_id) -> ResponseGetPost:
        async with self.async_session.begin() as session:
            post = await PostModel.read_by_id(session, post_id)

            like_key = f"post:{post_id}:likes"
            dislike_key = f"post:{post_id}:dislikes"

            if not redis.is_connected():
                # connect to redis host
                await redis.connect()

            likes = await redis.get(like_key)
            dislikes = await redis.get(dislike_key)

            return ResponseGetPost(
                post=Post.from_orm(post), likes=likes, dislikes=dislikes
            )


class CreatePostService(BaseService):
    async def execute(self, post: PostIn, user_id: int) -> Post:
        async with self.async_session.begin() as session:
            post = await PostModel.create(session, user_id, post.content)
            return Post.from_orm(post)


class UpdatePostService(PostAuthorizeMixin, BaseService):
    async def execute(self, post: PostInUpdate, user: UserModel) -> Post:
        async with self.async_session.begin() as session:
            post_db = await PostModel.read_by_id(session, post.post_id)

            if not post_db:
                raise HTTPException(status_code=404)

            # check if current user permission to update such object
            self.auth(post_db, user)

            await post_db.update(
                session, user_id=user.id, content=post.content
            )
            await session.refresh(post_db)
            return Post.from_orm(post_db)


class DeletePostService(PostAuthorizeMixin, BaseService):
    async def execute(self, post_id: int, user: UserModel) -> dict:
        async with self.async_session.begin() as session:
            post = await PostModel.read_by_id(session, post_id)

            if not post:
                raise HTTPException(status_code=404)

            # check if current user permission to update such object
            self.auth(post, user)

            await PostModel.delete(session, post)
            return {}


class LikePostService(BaseService):
    async def execute(self, post_id: int, current_user: UserModel) -> dict:
        async with self.async_session.begin() as session:
            # Check if the post exists
            post = await PostModel.read_by_id(session, post_id)

            if not post:
                raise HTTPException(status_code=404, detail="Post not found")

            # Check if the user has owns the post
            if post.user_id == current_user.id:
                raise HTTPException(
                    status_code=400, detail="User can not like his own post"
                )

            # Check if the user has already liked the post
            existing_like = await LikeModel.existing_like(
                session, post_id, current_user.id
            )

            if existing_like:
                raise HTTPException(
                    status_code=400, detail="You have already liked this post"
                )

            # delete dislike if exists
            dislike = await DislikeModel.existing_dislike(
                session, post_id, current_user.id
            )

            if dislike:
                await DislikeModel.delete(session, dislike)

            await self.update_cache(post_id, current_user)

            await LikeModel.create(
                session, post_id=post_id, user_id=current_user.id
            )
            return {"message": "Post liked successfully"}

    @staticmethod
    async def update_cache(post_id: int, current_user):
        if not redis.is_connected():
            await redis.connect()

        key = f"post:{post_id}:likes"
        post_users_likes_key = f"post:{post_id}:likes:users"

        dislike_key = f"post:{post_id}:dislikes"
        post_users_dislikes_key = f"post:{post_id}:dislikes:users"

        # Increment the number of likes for the post
        await redis.incr(key)

        # add user to likes set
        await redis.set(post_users_likes_key, current_user.id)

        # check if user disliked this post
        if current_user.id in await redis.get_set(post_users_dislikes_key):

            # decrement the dislikes for this post
            await redis.decr(dislike_key)

            # remove user from dislikes set
            await redis.srem(post_users_dislikes_key, current_user.id)


class UnLikePostService(BaseService):
    async def execute(self, post_id: int, current_user: UserModel) -> dict:
        async with self.async_session.begin() as session:
            # Check if the post exists
            post = await PostModel.read_by_id(session, post_id)

            if not post:
                raise HTTPException(status_code=404, detail="Post not found")

            # Check if the user has owns the post
            if post.user_id == current_user.id:
                raise HTTPException(
                    status_code=400, detail="User can not unlike his own post"
                )

            # Check if the user has already liked the post
            existing_like = await LikeModel.existing_like(
                session, post_id, current_user.id
            )

            if not existing_like:
                raise HTTPException(
                    status_code=400, detail="Post should be liked first"
                )

            key = f"post:{post_id}:likes"
            post_users_likes_key = f"post:{post_id}:likes:users"

            await redis.decr(key)
            await redis.srem(post_users_likes_key, current_user.id)

            await LikeModel.delete(session, existing_like)
            return {"message": "Post unliked successfully"}


class DisLikePostService(BaseService):
    async def execute(self, post_id: int, current_user: UserModel) -> dict:
        async with self.async_session.begin() as session:
            # Check if the post exists
            post = await PostModel.read_by_id(session, post_id)

            if not post:
                raise HTTPException(status_code=404, detail="Post not found")

            # Check if the user has owns the post
            if post.user_id == current_user.id:
                raise HTTPException(
                    status_code=400, detail="User can not dislike his own post"
                )

            # Check if the user has already disliked the post
            existing_dislike = await DislikeModel.existing_dislike(
                session, post_id, current_user.id
            )

            if existing_dislike:
                raise HTTPException(
                    status_code=400,
                    detail="You have already disliked this post",
                )

            # delete like if exists
            like = await DislikeModel.existing_dislike(
                session, post_id, current_user.id
            )

            if like:
                await LikeModel.delete(session, like)

            if not redis.is_connected():
                # connect to redis host
                await redis.connect()

            key = f"post:{post_id}:dislikes"
            like_key = f"post:{post_id}:likes"

            # Increment the number of dislikes for the post
            await redis.incr(key)

            # Remove the post from the likes set, if it exists
            await redis.decr(like_key)

            await DislikeModel.create(
                session, post_id=post_id, user_id=current_user.id
            )
            return {"message": "Post disliked successfully"}

    @staticmethod
    async def update_cache(post_id: int, current_user):
        if not redis.is_connected():
            await redis.connect()

        key = f"post:{post_id}:dislikes"
        post_users_dislikes_key = f"post:{post_id}:dislikes:users"

        like_key = f"post:{post_id}:likes"
        post_users_likes_key = f"post:{post_id}:likes:users"

        # Increment the number of dislikes for the post
        await redis.incr(key)

        # add user to dislikes set
        await redis.set(post_users_dislikes_key, current_user.id)

        # check if user disliked this post
        if current_user.id in await redis.get_set(post_users_likes_key):
            # decrement the likes for this post
            await redis.decr(like_key)

            # remove user from likes set
            await redis.srem(post_users_likes_key, current_user.id)


class UnDisLikePostService(BaseService):
    async def execute(self, post_id: int, current_user: UserModel) -> dict:
        async with self.async_session.begin() as session:
            # Check if the post exists
            post = await PostModel.read_by_id(session, post_id)

            if not post:
                raise HTTPException(status_code=404, detail="Post not found")

            # Check if the user has owns the post
            if post.user_id == current_user.id:
                raise HTTPException(
                    status_code=400,
                    detail="User can not undislike his own post",
                )

            # Check if the user has already disliked the post
            existing_dislike = await DislikeModel.existing_dislike(
                session, post_id, current_user.id
            )

            if not existing_dislike:
                raise HTTPException(
                    status_code=400, detail="Post should be disliked first"
                )

            if not redis.is_connected():
                # connect to redis host
                await redis.connect()

            key = f"post:{post_id}:dislikes"
            post_users_dislikes_key = f"post:{post_id}:dislikes:users"

            await redis.decr(key)
            await redis.srem(post_users_dislikes_key, current_user.id)

            await DislikeModel.delete(session, existing_dislike)
            return {"message": "Post undisliked successfully"}
