from pydantic import BaseModel
from typing import Optional

class UserProfile(BaseModel):
    first_name: str
    last_name: str
    role: str = 'member'
    slot: int = 1
    registered: bool = False