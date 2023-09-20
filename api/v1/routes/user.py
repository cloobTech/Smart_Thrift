from fastapi import APIRouter, Depends, HTTPException, status
from ..utils import get_db
from models.user import User
from models.user_profile import UserProfile
from sqlalchemy.orm import Session
from schemas.user import CreateUser as CreateUserSchema

router = APIRouter(tags=['Users'], prefix='/users')


@router.get('/')
def get_users(storage: Session = Depends(get_db)) -> list[dict | None]:
    """Return all users instances as a list of dictionary from the database"""
    users: list = []
    all_users: dict = storage.all(User)
    if not all_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    for key in all_users.keys():
        user = (all_users[key].to_dict())
        users.append(user)
    return (users)


@router.get('/{id}')
def get_user(id: str, storage: Session = Depends(get_db)) -> dict:
    """Return a single user instances as a dictionary from the database"""
    user: dict = storage.get(User, id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    user = user.to_dict()
    return user


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(user_details: CreateUserSchema, storage: Session = Depends(get_db)) -> dict:
    """Create a new user"""
    user_dict: dict = user_details.model_dump()
    _user = user_dict['user']
    profile = user_dict['profile']
   
    user = storage.get_by_email(_user['email']) #check if user exists in DB
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    new_user = User(**_user)

    # create user profile
    user_profile = UserProfile(**profile, user=new_user)
    user_profile.save()
    return {"message": "User successfully created"}