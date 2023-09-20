"""User Model Schema"""
from pydantic import BaseModel
from schemas.user_profile import UserProfile
from typing import Optional, Dict

class User(BaseModel):
    email: str
    password: str
    reset_token: Optional[str | None] = None 


class CreateUser(BaseModel):
    user: User
    profile: UserProfile