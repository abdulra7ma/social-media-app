from fastapi import APIRouter, Depends

from app.db_models.user import UserModel
from app.models.post import PostIn, Post, PostInUpdate, ResponseGetPost
from app.services.post import (
    CreatePostService,
    UpdatePostService,
    DeletePostService,
    LikePostService,
    UnLikePostService,
    DisLikePostService,
    UnDisLikePostService,
    GetPostService,
)
from app.utils.user import get_current_user

router = APIRouter()


@router.get("/{post_id}", response_model=ResponseGetPost)
async def get_post(
    post_id: int,
    # current_user: UserModel = Depends(get_current_user),
    service: GetPostService = Depends(GetPostService),
):
    return await service.execute(post_id)


@router.post("", response_model=Post)
async def create_post(
    post: PostIn,
    current_user: UserModel = Depends(get_current_user),
    service: CreatePostService = Depends(CreatePostService),
):
    return await service.execute(post, current_user.id)


@router.put("", response_model=Post)
async def update_post(
    post: PostInUpdate,
    current_user: UserModel = Depends(get_current_user),
    service: UpdatePostService = Depends(UpdatePostService),
):
    return await service.execute(post, current_user)


@router.delete("")
async def delete_post(
    post_id: int,
    current_user: UserModel = Depends(get_current_user),
    service: DeletePostService = Depends(DeletePostService),
):
    return await service.execute(post_id, current_user)


@router.post("/{post_id}/like")
async def like_post(
    post_id: int,
    current_user: UserModel = Depends(get_current_user),
    service: LikePostService = Depends(LikePostService),
):
    return await service.execute(post_id, current_user)


@router.delete("/{post_id}/unlike")
async def unlike_post(
    post_id: int,
    current_user: UserModel = Depends(get_current_user),
    service: UnLikePostService = Depends(UnLikePostService),
):
    return await service.execute(post_id, current_user)


@router.post("/{post_id}/dislike")
async def dislike_post(
    post_id: int,
    current_user: UserModel = Depends(get_current_user),
    service: DisLikePostService = Depends(DisLikePostService),
):
    return await service.execute(post_id, current_user)


@router.delete("/{post_id}/undislike")
async def undislike_post(
    post_id: int,
    current_user: UserModel = Depends(get_current_user),
    service: UnDisLikePostService = Depends(UnDisLikePostService),
):
    return await service.execute(post_id, current_user)
