from fastapi import APIRouter, Depends, HTTPException, status
from ..utils import get_db
from models.user_profile import UserProfile
from sqlalchemy.orm import Session

router = APIRouter(tags=['Users_Profile'], prefix='/profile')


@router.get('/')
def get_users(storage: Session = Depends(get_db)) -> list[dict | None]:
    """Return all user profiles instances as a list of dictionary from the database"""
    users: list = []
    all_users: dict = storage.all(UserProfile)
    if not all_users:
        return users
    for key in all_users.keys():
        user = (all_users[key].to_dict())
        users.append(user)
    return (users)


@router.get('/{id}')
def get_user(id: str, storage: Session = Depends(get_db)) -> dict:
    """Return a single user profile instances as a dictionary from the database"""
    user: dict = storage.get(UserProfile, id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User's profile not found")
    user = user.to_dict()
    return user
