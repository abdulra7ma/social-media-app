from pydantic import BaseModel


class PostIn(BaseModel):
    content: str


class PostInUpdate(BaseModel):
    post_id: int
    content: str

    class Config:
        schema_extra = {
            "example": {"post_id": 1, "content": "post updated content"}
        }


class Post(BaseModel):
    id: int
    user_id: int
    content: str

    class Config:
        orm_mode = True


class ResponseGetPost(BaseModel):
    post: Post
    likes: int = 0
    dislikes: int = 0


class Like(BaseModel):
    id: int
    post_id: int
    user_id: int

    class Config:
        orm_mode = True


class LinkIn:
    post_id: int


class Dislike(BaseModel):
    post_id: int
    user_id: int


class DislikeIn:
    post_id: int
