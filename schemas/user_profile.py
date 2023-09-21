from pydantic import BaseModel
from schemas.contribution import Contribution


class UserProfile(BaseModel):
    first_name: str
    last_name: str
    role: str = 'member'
    slot: int = 1
    registered: bool = False
    month_covered: int = 0


class UserProfileOut(UserProfile):
    contributions: Contribution
