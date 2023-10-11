from pydantic import BaseModel, EmailStr
from schemas.contribution import Contribution
from datetime import datetime


class UserProfile(BaseModel):
    first_name: str
    last_name: str
    role: str = 'member'
    slot: int = 1
    registered: bool = False
    month_covered: int = 0
    id: str


class UserProfileOut(UserProfile):
    contributions: Contribution


class Test(UserProfile):
    email: EmailStr
    create_at: str
