from fastapi import APIRouter, Depends, HTTPException, status
from ..utils import get_db
from models.contribution import Contribution
from models.user_profile import UserProfile
from sqlalchemy.orm import Session
from schemas.contribution import ContributionSchema, DeleteContr, UpdateContr

router = APIRouter(tags=['Contribution'], prefix='/contributions')


@router.get('/')
def get_users(storage: Session = Depends(get_db)) -> list[dict | None]:
    """Return all user contribution instances as a list of dictionary from the database"""
    contributions: list = []
    all_contributions: dict = storage.all(Contribution)
    if not all_contributions:
        return contributions
    contributions = [all_contributions[key].to_dict() for key in all_contributions]
    return (contributions)


@router.get('/{id}')
def get_user(id: str, storage: Session = Depends(get_db)) -> dict:
    """Return a single user profile instances as a dictionary from the database"""
    contribution: dict = storage.get(Contribution, id)
    if contribution is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contribution instance not found")
    contribution = contribution.to_dict()
    return contribution


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_contribution(data: ContributionSchema, storage: Session = Depends(get_db)) -> dict:
    """Create a new contribution instance"""
    SUBSCRIPTION: int = 10000  # montly contribution per slot

    data_dict = data.model_dump()
    profile_id = data_dict['profile_id']
    contribution_data = data_dict['contribution_data']

    user = storage.get(UserProfile, profile_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User profile not found")

    # create a new contribution and link it to the user
    contribution = Contribution(**contribution_data)

    # Calculate a user's contribution and determine advance payment
    user_dict: dict = user.to_dict()
    contribution_dict: dict = contribution.to_dict()
    amount = contribution_dict.get('amount', 0)
    slot = user_dict.get('slot', 1)
    month_covered = user_dict.get('month_covered')
    total_sub = SUBSCRIPTION * slot
    _month_covered = int(amount/total_sub) + month_covered
    user_dict['month_covered'] = _month_covered

    # update DB
    try:
        user.update(user_dict)
        user.contributions.append(contribution)
        contribution.save()
        return {"message": "Transaction Successful"}
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Bad Request')


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_contribution(data: DeleteContr, storage: Session = Depends(get_db)) -> None:
    """Delete a contribution instance"""

    # why I'm not using a url parameter to delete the resource:
    # I'm using a <data> - json body instead - because I want to carry out
    #  other operations with other classes before deletion

    SUBSCRIPTION: int = 10000  # montly contribution per slot
    data_dict: dict = data.model_dump()
    profile_id = data_dict['profile_id']
    contribution_id = data_dict['contribution_id']

    # Get the contribution and it's corresponding user_profile instance
    # calculate how much was recorded
    # then update the user profile's month contribution attribute (month_covered)
    contribution = storage.get(Contribution, contribution_id)
    user = storage.get(UserProfile, profile_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    if contribution is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Contribution not found')

    # Calculate contribution
    contribution_dict = contribution.to_dict()
    if contribution_dict['member_id'] != profile_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Cannot associate User with Contribution instance')
    amount = contribution_dict.get('amount', 0)

    # Calculate month covered
    user_dict = user.to_dict()
    slot = user_dict.get('slot', 1)
    month_covered = user_dict.get('month_covered')
    total_sub = SUBSCRIPTION * slot
    _month_covered = month_covered - int(amount/total_sub)
    user_dict['month_covered'] = _month_covered

    try:
        # update DB
        user.update(user_dict)
        contribution.delete()
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='List Errors')


@router.put('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def update_contribution(id: str, data: UpdateContr, storage: Session = Depends(get_db)):
    """Update a <Contribution> instance"""
    SUBSCRIPTION: int = 10000  # montly contribution per slot
    data_dict: dict = data.model_dump()
    profile_id = data_dict['profile_id']
    contribution_data: dict = data_dict['contribution_data']

    contribution = storage.get(Contribution, id)
    user = storage.get(UserProfile, profile_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    if contribution is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Contribution not found')

    contribution_dict = contribution.to_dict()
    if contribution_dict['member_id'] != profile_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Cannot associate User with Contribution instance')

    # Update Profile & Contribution
    # Get the user's prev's contribution amount and profile current month-covered
    # Calculate how many months the prev amount covered and deduct the month from (month-covered)
    # Finanlly, get new contribution, calculate and update user's profile
    user_dict = user.to_dict()
    prev_amount = contribution_dict.get('amount', 0)
    new_amount = contribution_data.get('amount', 0)
    slot = user_dict.get('slot', 1)
    total_sub = SUBSCRIPTION * slot
    month_covered = user_dict.get('month_covered')
    month_covered = month_covered - int(prev_amount/total_sub)
    _month_covered = int(new_amount/total_sub) + month_covered
    user_dict['month_covered'] = _month_covered

    user.update(user_dict)
    contribution.update(contribution_data)

    return {}
    # Why I'm not using url parameters - (see the delete function)
