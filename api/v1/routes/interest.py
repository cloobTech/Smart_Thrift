"""Handle Interest on Loan Refund"""
from fastapi import APIRouter, Depends, HTTPException, status
from ..utils import get_db
from models.interest import Interest
from sqlalchemy.orm import Session

router = APIRouter(tags=['Interest'], prefix='/interest')

@router.get('/')
def get_interests(storage: Session = Depends(get_db)) -> list[dict | None]:
    """Return all instances of <Interest> as a list of dictionary from the database"""
    interest: list = []
    all_interest: dict = storage.all(Interest)
    if not all_interest:
        return interest
    interest = [all_interest[key].to_dict() for key in all_interest.keys()]
    return interest


@router.get('/{id}')
def get_interest(id: str, storage: Session = Depends(get_db)) -> dict:
    """Return a single instance of <Interest> as a dictionary from the database"""
    interest: dict = storage.get(Interest, id)
    if interest is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="<Loan Refund Instance> not found")
    interest = interest.to_dict()
    return interest