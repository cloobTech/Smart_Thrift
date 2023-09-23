"""All loan related activies are linked to Loan Model"""

from fastapi import APIRouter, Depends, HTTPException, status
from ..utils import get_db
from models.loan import Loan
from models.loan_out import LoanOut
from models.user_profile import UserProfile
from sqlalchemy.orm import Session
from schemas.loan import LoanSchema

router = APIRouter(tags=['Loan'], prefix='/loan')


@router.get('/')
def get_loans(storage: Session = Depends(get_db)) -> list[dict | None]:
    """Return all [aggregate] loan instances as a list of dictionary from the database"""
    loans: list = []
    all_loans: dict = storage.all(Loan)
    if not all_loans:
        return loans
    loan = [all_loans[key].to_dict() for key in all_loans.keys()]
    return loan


@router.get('/{id}')
def get_loan(id: str, storage: Session = Depends(get_db)) -> dict:
    """Return a single aggregate loan instances as a dictionary from the database"""
    loan: dict = storage.get(Loan, id)
    if loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User's profile not found")
    loan = loan.to_dict()
    return loan


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_loan(data: LoanSchema, storage: Session = Depends(get_db)) -> dict:
    """Create a new loan instance"""
    data = data.model_dump()
    loan_data = data['loan_data']
    loanout_data = data['loanout_data']
    others = data['others']

    is_new = others['is_new']
    guarantor_id = others['guarantor_id']
    loan_id = others['loan_id']

    # Create Loan
    # The idea is to create a new loan instance if the debtor hasn't collected
    # any loans before else we just update the user's outstanding loan
    if is_new:
        # Get Guarantor
        guarantor = storage.get(UserProfile, guarantor_id)
        if guarantor is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User profile not found")
        loan = Loan(**loan_data)
        guarantor.loan.append(loan)  # link loan to user
    else:
        loan = storage.get(Loan, loan_id)
        if loan is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Loan instance not found")

    loan_dict: dict = loan.to_dict()

    # # create loan out
    loan_out = LoanOut(**loanout_data)

    # update total_amount of Loan instance
    total_amount = loan_dict.get('total_amount', 0)
    total_amount = total_amount + loanout_data['amount']
    loan_dict['total_amount'] = total_amount

    loan.update(loan_dict)
    loan.loan_out.append(loan_out)
    loan_out.save()

    return {"message": "Operation Successful"}


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_loan(id: str, storage: Session = Depends(get_db)) -> None:
    """Delete an aggregate loan instance"""
    loan: dict = storage.get(Loan, id)
    if loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Loan instance not found")
    loan.delete()


@router.put('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def update_loan(id: str, data: dict, storage: Session = Depends(get_db)):
    """Update a loan instance"""
    if len(data) < 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='request data is empty'
        )
    loan: dict = storage.get(Loan, id)
    if loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User's profile not found")
    loan.update(data)

    return {}
