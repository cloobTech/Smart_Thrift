from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Loan(BaseModel):
    is_member: bool
    first_name: str
    last_name: str


class LoanOut(BaseModel):
    start_date: datetime
    end_date: datetime
    amount: float


class Others(BaseModel):
    is_new: bool
    guarantor_id: Optional[str] = ''
    loan_id: Optional[str] = ''
    loan_profile_id: Optional[str] = ''


class LoanSchema(BaseModel):
    loan_data: Loan
    loanout_data: LoanOut
    others: Others

    #----------------------------------------------------- Loan -------------------------------

class ParentIds(BaseModel):
    loan_id: Optional[str]
    loan_profile_id: Optional[str]

class LoanOutData(BaseModel):
    start_date: Optional[datetime] = None
    end_date:Optional[datetime] = None
    amount: Optional[float]


class LoanOutUpdate(BaseModel):
    parent_ids: ParentIds
    loanout_data: LoanOutData