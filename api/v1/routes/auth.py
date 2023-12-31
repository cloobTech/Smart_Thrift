from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.auth.auth import Auth

router = APIRouter(tags=['Authentication'], prefix='/auth')

AUTH = Auth()


@router.post('/', status_code=status.HTTP_201_CREATED)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    """Handle Logging in a user"""
    token_dict: dict[str, str] = AUTH.valid_login(
        user_credentials.username, user_credentials.password)
    if not token_dict:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')

    return token_dict
