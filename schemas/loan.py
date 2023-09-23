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


class LoanSchema(BaseModel):
    loan_data: Loan
    loanout_data: LoanOut
    others: Others