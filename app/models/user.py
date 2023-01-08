from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "Adam",
                "email": "adam@hotmail.com",
                "password": "faroko1987",
            }
        }
        extra = "forbid"


class SignUpResponseModel(BaseModel):
    message: str = "Successfully created user"
    # access_token: str


class LoginSchema(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "Adam",
                "password": "faroko1987",
            }
        }
