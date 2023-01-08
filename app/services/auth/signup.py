import requests
from fastapi import HTTPException

from app.core.config import settings
from app.models.user import User
from app.selectors.user import get_user_by_username
from app.services.user import UserService
from app.utils.password import get_password_hash
from ..base import BaseService


class SignupService(BaseService):
    async def execute(self, user: User):
        async with self.async_session.begin() as session:
            db_user = await get_user_by_username(user.username, session)

            if db_user:
                raise HTTPException(
                    status_code=400, detail="Username already registered"
                )

            # Verify the email address using Email-hunter
            url = f"https://api.hunter.io/v2/email-verifier?email={user.email}&api_key={settings.EMAILHUNTER_API_KEY}"
            emailhunter_response = requests.get(url)

            if emailhunter_response.status_code != 200:
                raise HTTPException(
                    status_code=400, detail="Error verifying email address"
                )

            # hash the user password
            hashed_password = get_password_hash(user.password)
            user = User(
                username=user.username,
                password=hashed_password,
                email=user.email,
            )

            # create new user
            await UserService().create(user=user, session=session)
            return True
