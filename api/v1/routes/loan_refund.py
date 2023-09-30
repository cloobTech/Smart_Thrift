"""Handle Loan Refund Activities"""

from fastapi import APIRouter, Depends, HTTPException, status
from ..utils import get_db
from models.interest import Interest
from models.loan_refund import LoanRefund
from models.loan_profile import LoanProfile
from models.user_profile import UserProfile
from models.loan import Loan
from sqlalchemy.orm import Session

router = APIRouter(tags=['LoanRefund'], prefix='/refunds')


@router.get('/')
def get_refunds(storage: Session = Depends(get_db)) -> list[dict | None]:
    """Return all instances of loan refunded as a list of dictionary from the database"""
    refunds: list = []
    all_loan_refunds: dict = storage.all(LoanRefund)
    if not all_loan_refunds:
        return refunds
    refunds = [all_loan_refunds[key].to_dict()
               for key in all_loan_refunds.keys()]
    return refunds


@router.get('/{id}')
def get_refund(id: str, storage: Session = Depends(get_db)) -> dict:
    """Return a single instance of <Loan Refund> as a dictionary from the database"""
    refund: dict = storage.get(LoanRefund, id)
    if refund is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="<Loan Refund Instance> not found")
    refund = refund.to_dict()
    return refund


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_refund(data: dict, storage: Session = Depends(get_db)) -> dict:
    """Create a new <Loan Refund> instance"""
    loan_profile_id = data['loan_profile_id']
    refund_data = data['refund_data']

    # Made sure I can get the loan and loan profile instances linked to the new refund
    loan_profile = storage.get(LoanProfile, loan_profile_id)
    if loan_profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="<Loan Profile> instance not found")

    loan_id = loan_profile.to_dict()['loan_id']
    loan = storage.get(Loan, loan_id)
    if loan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="<Loan> instance not found")

    loan_dict = loan.to_dict()
    loan_profile_dict = loan_profile.to_dict()

    # Create the refund object
    # Calculate (Deduct) Principal and Interest
    refund = LoanRefund(**refund_data)
    amount_refunded = refund.to_dict()['amount']
    principal_cleared = amount_refunded - loan_profile_dict.get('interest')
    _interest = amount_refunded - principal_cleared
    interest_dict = {"amount": _interest}

    # ------------------Deduct refund from loan
    loan_dict['total_amount'] = loan_dict['total_amount'] - principal_cleared

    # check if loan has been cleared
    loan_profile_data = {}
    if loan_dict['total_amount'] <= 0:
        loan_profile_data['status'] = True
        loan_dict['total_amount'] = 0

    if loan_dict['is_member']:  # Interest rate on loans
        RATE = 0.05
    else:
        RATE = 0.1

    loan_profile_data['principal'] = loan_dict['total_amount']
    loan_profile_data['interest'] = loan_dict['total_amount'] * RATE
    loan_profile_data['total'] = loan_dict['total_amount'] + \
        loan_profile_data['interest']

    try:
        loan_profile.update(loan_profile_data)
        loan.update(loan_dict)
        loan.loan_refund.append(refund)

        # Create Interest Class and link it to refund
        # Link interest to Guarantor (Member)

        interest = Interest(**interest_dict, refund=refund)
        guarantor = storage.get(UserProfile, loan_dict['guarantor_id'])
        if guarantor is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='<Guarantor/User> not found')
        guarantor.interest.append(interest)

        interest.save()
        refund.save()
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Database couldn't complete transaction")

    return {"message": "Operation Successful"}


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_refund(id: str, data: dict, storage: Session = Depends(get_db)):
    """deletes an instance of <Refund> object"""
    loan_profile_id = data.get("loan_profile_id")
    interest_id = data.get('interest_id')

    loan_profile = storage.get(LoanProfile, loan_profile_id)
    if loan_profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="<Loan Profile> instance not found")

    loan_id = loan_profile.to_dict()['loan_id']
    loan = storage.get(Loan, loan_id)
    if loan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="<Loan Profile> instance not found")

    refund = storage.get(LoanRefund, id)
    if refund is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="<Refund> instance not found")

    interest = storage.get(Interest, interest_id)
    if interest is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="<Interest> instance not found")

    refund_dict = refund.to_dict()
    loan_profile_dict = loan_profile.to_dict()
    loan_dict = loan.to_dict()
    interest_dict = interest.to_dict()

    # Update Loan and Loan Ptofile
    refund_amount = refund_dict['amount'] - interest_dict['amount']
    loan_total = loan_dict['total_amount']
    loan_total = loan_total + refund_amount
    loan_dict['total_amount'] = loan_total

    if loan_dict['is_member']:  # Interest rate on loans
        RATE = 0.05
    else:
        RATE = 0.1

    loan_profile_dict['principal'] = loan_dict['total_amount']
    loan_profile_dict['interest'] = loan_dict['total_amount'] * RATE
    loan_profile_dict['total'] = loan_dict['total_amount'] + \
        loan_profile_dict['interest']

    try:
        refund.delete()
        loan.update(loan_dict)
        loan_profile.update(loan_profile_dict)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Database couldn't complete transaction")


# TO BE REVIEWED
# @router.put('/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def update_loan(id: str, data: dict, storage: Session = Depends(get_db)):
#     """Update a refund instance"""
#     loan_profile_id = data.get("loan_profile_id")
#     interest_id = data.get('interest_id')
#     refund_data = data.get('refund_data')

#     refund = storage.get(LoanRefund, id)
#     if refund is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="<Refund> instance not found")

#     loan_profile = storage.get(LoanProfile, loan_profile_id)
#     if loan_profile is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="<Loan Profile> instance not found")

#     loan_id = loan_profile.to_dict()['loan_id']
#     loan = storage.get(Loan, loan_id)
#     if loan is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="<Loan Profile> instance not found")

#     interest = storage.get(Interest, interest_id)
#     if interest is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="<Interest> instance not found")

#     refund_dict = refund.to_dict()
#     loan_profile_dict = loan_profile.to_dict()
#     loan_dict = loan.to_dict()
#     interest_dict = interest.to_dict()

#     # Update Loan and Loan Ptofile
#     refund_amount = refund_dict['amount'] - interest_dict['amount']
#     loan_dict['total_amount'] += refund_amount
#     updated_amount = refund_data['amount'] - loan_profile_dict['interest']
#     loan_dict['total_amount'] -= updated_amount

#     if loan_dict['is_member']:  # Interest rate on loans
#         RATE = 0.05
#     else:
#         RATE = 0.1

#     loan_profile_dict['principal'] = loan_dict['total_amount']
#     loan_profile_dict['interest'] = loan_dict['total_amount'] * RATE
#     loan_profile_dict['total'] = loan_dict['total_amount'] + \
#         loan_profile_dict['interest']

#     if refund_data['amount'] >= loan_profile_dict['interest']:
#         interest_dict['amount'] = loan_profile_dict['interest']
#     else:
#         interest_dict['amount'] = abs(
#             refund_data['amount'] - loan_profile_dict['interest'])

#     try:
#         interest.update(interest_dict)
#         refund.update(refund_data)
#         loan.update(loan_dict)
#         loan_profile.update(loan_profile_dict)
#     except Exception:
#         raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                             detail="Database couldn't complete transaction")
