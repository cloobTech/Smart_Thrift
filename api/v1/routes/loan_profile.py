"""
This module will handle updating debtor's loan profile
- It will update the profile table when a new loan loan is taken,
- when a debtor adds more loan to an existing loan or when
- a refund comes in.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from ..utils import get_db
from models.loan import Loan
from models.loan_profile import LoanProfile
from sqlalchemy.orm import Session

router = APIRouter(tags=['LoanProfile'], prefix='/loan_profile')


@router.get('/')
def get_loans_profile(storage: Session = Depends(get_db)) -> list[dict | None]:
    """Return all loan_profile instances as a list of dictionary from the database"""
    loans: list = []
    all_loans: dict = storage.all(LoanProfile)
    if not all_loans:
        return loans
    loan = [all_loans[key].to_dict() for key in all_loans.keys()]
    return loan


@router.get('/{id}')
def get_loan(id: str, storage: Session = Depends(get_db)) -> dict:
    """Return a single loan_profile instances as a dictionary from the database"""
    loan: dict = storage.get(LoanProfile, id)
    if loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Loan instance not found")
    loan = loan.to_dict()
    return loan
