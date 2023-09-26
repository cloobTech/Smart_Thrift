from fastapi import APIRouter, Depends, HTTPException, status
from ..utils import get_db
from models.loan import Loan
from models.loan_out import LoanOut
from sqlalchemy.orm import Session


router = APIRouter(tags=['LoanOut'], prefix='/loan_out')


@router.get('/')
def get_loans(storage: Session = Depends(get_db)) -> list[dict | None]:
    """Return all [individual] loan instances as a list of dictionary from the database"""
    loans: list = []
    all_loans: dict = storage.all(LoanOut)
    if not all_loans:
        return loans
    loan = [all_loans[key].to_dict() for key in all_loans.keys()]
    return loan


@router.get('/{id}')
def get_loan(id: str, storage: Session = Depends(get_db)) -> dict:
    """Return a single loan instances as a dictionary from the database"""
    loan: dict = storage.get(LoanOut, id)
    if loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Loan instance not found")
    loan = loan.to_dict()
    return loan


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_loan(id: str, loan_id: dict, storage: Session = Depends(get_db)) -> None:
    """Delete a loan instance and update the aggregate (parent) loan"""
    loan_id = loan_id.get('loan_id')
    loan = storage.get(Loan, loan_id)
    loan_out = storage.get(LoanOut, id)
    if loan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Aggregate Loan instance not found")
    if loan_out is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Loan instance not found")

    loan_dict: dict = loan.to_dict()
    loanout_dict: dict = loan_out.to_dict()

    if loan_id != loanout_dict['loan_id']:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Couldn't link loan instance to aggregate loan")
    total_amount = loan_dict['total_amount'] - loanout_dict['amount']
    loan_dict['total_amount'] = total_amount
    loan_out.delete()

    # if parent instance of loan less or equals - we delete the loan
    # because it implies that the aggregate loan doesn't have a child
    # instance else we update
    if loan_dict['total_amount'] <= 0:
        loan.delete()
    else:
        loan.update(loan_dict)


@router.put('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def update_loan(id: str, data: dict, storage: Session = Depends(get_db)):
    """Update a loan instance"""


def update_loanout(id: str, data: dict, storage: Session = Depends(get_db)):
    """Update a loan instance"""
    if len(data) < 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='request data is empty'
        )

    loanout_data: dict = data['loanout_data']
    loan_out = storage.get(LoanOut, id)

    # I only want to update the Parent Loan if it is "amount" that's
    # been updated
    if 'amount' in loanout_data:
        parent_id: dict = data['parent_id']
        loan_id = parent_id.get('loan_id')
        loan = storage.get(Loan, loan_id)

        if loan is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Aggregate Loan instance not found")
        loan_dict: dict = loan.to_dict()

    if loan_out is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Loan instance not found")

    loanout_dict: dict = loan_out.to_dict()

    if 'amount' in loanout_data:
        if loan_id != loanout_dict['loan_id']:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Couldn't link loan instance to aggregate loan")
        total_amount = loan_dict['total_amount'] - loanout_dict['amount']
        total_amount += loanout_data['amount']
        loan_dict['total_amount'] = total_amount
        loan.update(loan_dict)

    loan_out.update(loanout_data)

    return {}
