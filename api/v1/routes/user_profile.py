from fastapi import APIRouter, Depends, HTTPException, status, Query
from ..utils import get_db, hyper_media_pagination
from models.user_profile import UserProfile
from sqlalchemy.orm import Session
from typing import Any
from models.auth.auth import Auth
from schemas.user_profile import Test

AUTH = Auth()


router = APIRouter(tags=['Users_Profile'], prefix='/profile')


@router.get('/')
def get_users(page: int = 1, page_size: int = 7, current_user: UserProfile = Depends(AUTH.get_current_user), column: str | None = None, search_string: str | None = None) -> dict[str, Any]:
    """Return all user profiles instances as a list of dictionary from the database"""
    if current_user.role != 'admin' and current_user.role != 'owner':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Access")

    users: list = []
    all_users: dict = hyper_media_pagination(
        UserProfile, page=page, page_size=page_size, column=column, search=search_string)
    if not all_users:
        return users
    return (all_users)


@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_user(id: str, storage: Session = Depends(get_db), current_user: UserProfile = Depends(AUTH.get_current_user)) -> dict:
    """Return a single user profile instances as a dictionary from the database"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Access")
    user: dict = storage.get(UserProfile, id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User's profile not found")
    user_dict = user.to_dict()
    user_dict['email'] = user.user.email
    return user_dict


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: str, storage: Session = Depends(get_db)):
    """Delete a user"""
    user: dict = storage.get(UserProfile, id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    user.delete()


@router.put('/{id}', status_code=status.HTTP_201_CREATED)
def update_user(id: str, data: dict, storage: Session = Depends(get_db)) -> dict:
    """Update details of a user"""
    user: dict = storage.get(UserProfile, id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User's profile not found")
    user.update(data)
    user = user.to_dict()
    return user
