"""User Model Schema"""
from pydantic import BaseModel
from schemas.user_profile import UserProfile

class User(BaseModel):
    email: str
    password: str
    reset_token: str | None = None 


class CreateUser(BaseModel):
    user: User
    profile: UserProfile