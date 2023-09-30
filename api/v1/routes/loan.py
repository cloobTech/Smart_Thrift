"""All loan related activities are linked to Loan Model"""

from fastapi import APIRouter, Depends, HTTPException, status
from ..utils import get_db
from models.loan import Loan
from models.loan_out import LoanOut
from models.loan_profile import LoanProfile
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
    """Return a single aggregate loan instance as a dictionary from the database"""
    loan: dict = storage.get(Loan, id)
    if loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="<Loan Instance> not found")
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
    loan_profile_id = others['loan_profile_id']

    # Create Loan
    # The idea is to create a new loan instance if the debtor hasn't collected
    # any loans before else we just update the user's outstanding loan
    if is_new:
        # Get Guarantor
        guarantor = storage.get(UserProfile, guarantor_id)
        if guarantor is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="<User profile> not found")

        # If it's a new loan - I want to get the name from the
        # Guarantor's obj. Technically, A member who takes a loan guarantee's
        # him/herself - they don't need a third party guarantor
        loan = Loan(**loan_data)
        guarantor.loan.append(loan)  # link loan to user
    else:
        loan = storage.get(Loan, loan_id)
        if loan is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="<Loan Instance> not found")

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

    # After Creating or Updating a Loan Instance -
    # That instance should be updated in the Loan Profile's Table

    if loan_dict['is_member']:  # Interest rate on loans
        RATE = 0.05
    else:
        RATE = 0.1

    loan_profile_data = {}
    loan_profile_data['principal'] = loan_dict['total_amount']
    loan_profile_data['interest'] = loan_dict['total_amount'] * RATE
    loan_profile_data['total'] = loan_dict['total_amount'] + \
        loan_profile_data['interest']

    if is_new:  # if it's a new loan - create a new profile for the loan
        loan_profile = LoanProfile(**loan_profile_data, loan=loan)
    else:
        # Get exiting loan_profile and update it
        loan_profile = storage.get(LoanProfile, loan_profile_id)
        if loan_profile is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="<Loan Profile> instance not found")

        if loan_profile.to_dict()['loan_id'] != loan_dict['id']:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Cannot attach <Loan Profile Instance> to <Loan Instance>")

        loan_profile.update(loan_profile_data)

    loan_profile.save()
    return {"message": "Operation Successful"}


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_loan(id: str, storage: Session = Depends(get_db)) -> None:
    """Delete an aggregate loan instance"""
    loan: dict = storage.get(Loan, id)
    if loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="<Loan Instance> not found")
    loan.delete()


@router.put('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def update_loan(id: str, data: dict, storage: Session = Depends(get_db)):
    """Update a loan instance"""
    loan_data = data['loan_data']
    if len(data or loan_data) < 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='request data is empty'
        )
    loan: dict = storage.get(Loan, id)
    if loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User's profile not found")
    loan.update(loan_data)

    return {}
