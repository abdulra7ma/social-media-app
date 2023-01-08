from fastapi import HTTPException

from app.models.user import User, LoginSchema
from app.selectors.user import get_user_by_username
from app.utils.jwt import create_access_token
from app.utils.password import verify_password
from ..base import BaseService


class SignInService(BaseService):
    async def execute(self, login: LoginSchema):
        async with self.async_session.begin() as session:
            db_user = await get_user_by_username(login.username, session)

            if not db_user:
                raise HTTPException(
                    status_code=400, detail="User does not exists"
                )

            if not verify_password(login.password, db_user.password):
                raise HTTPException(
                    status_code=400, detail="Incorrect username or password"
                )

            # generate access token for the newly created user
            access_token = create_access_token(data={"user_id": db_user.id})

            return {"access_token": access_token}
