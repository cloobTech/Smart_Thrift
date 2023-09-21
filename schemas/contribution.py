from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Contribution(BaseModel):
    amount: float
    date: Optional[datetime] = datetime.utcnow()


class ContributionSchema(BaseModel):
    profile_id: str
    contribution_data: Contribution


class DeleteContr(BaseModel):
    profile_id: str
    contribution_id: str


class Amount(BaseModel):
    amount: float


class UpdateContr(BaseModel):
    profile_id: str
    contribution_data: Amount
