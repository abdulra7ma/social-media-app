from fastapi import APIRouter, Depends, Response

from app.models.token import AccessToken
from app.models.user import User, SignUpResponseModel, LoginSchema
from app.services.auth import SignupService, SignInService

router = APIRouter()


@router.post("/signup", response_model=SignUpResponseModel)
async def signup(
    user: User,
    service: SignupService = Depends(SignupService),
):
    await service.execute(user=user)
    return {"message": "Successfully created user"}


@router.post("/signin", response_model=AccessToken)
async def signup(
    login: LoginSchema,
    service: SignInService = Depends(SignInService),
):
    return await service.execute(login=login)
