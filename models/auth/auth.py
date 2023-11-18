#!/usr/bin/python3
"""
    Module to handle all forms of user authentication and authorization
"""
import bcrypt
import logging
from datetime import datetime, timedelta
import models
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models.user_profile import UserProfile
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import Session

SECRET_KEY = "Super_Secret_Key"
ALGORITHM = "HS256"
EXPIRATION_TIME = 250

outh2_scheme = OAuth2PasswordBearer(tokenUrl='auth')


class Auth:
    """
        Auth Class to interact with the authentication DB
    """

    def __create_access_token(self, data: dict) -> str:
        """Create A New Jwt Access Token"""
        to_encode = data.copy()

        expire = datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode, SECRET_KEY, ALGORITHM)  # returns a token
        return encoded_jwt

    def valid_login(self, email: str, password: str) -> dict[str, str] | None:
        """Validate a user's credentials"""
        if not email or type(email) != str:
            raise InvalidRequestError("Invalid Email Format")
        if not password or type(password) != str:
            raise InvalidRequestError("Invalid Password Format")
        try:
            user = models.storage.get_by_email(email)
            if not user:
                raise NoResultFound("User Not Found!")
            hashed_pwd = user.password.encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), hashed_pwd):

                # Creat a Jwt Token if user and password is correct
                data_to_encode: dict = {
                    "user_id": user.user_profile.id, "role": user.user_profile.role}
                token = self.__create_access_token(data_to_encode)

                return {"token": token, "token-type": "Bearer"}
        except NoResultFound:
            pass
        return False

    def verify_access_token(self, token: str, credential_exceptions):
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload is None:
                raise credential_exceptions
            return payload

        except JWTError:
            raise credential_exceptions

    def get_current_user(self, token: str = Depends(outh2_scheme)) -> UserProfile:
        """Get Current Logged in User"""
        credential_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                              detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

        payload: dict = self.verify_access_token(token, credential_exceptions)
        current_user = models.storage.get(UserProfile, payload['user_id'])
        return current_user

    def get_current_registered_user(self, current_user: UserProfile = Depends(get_current_user)) -> UserProfile:
        """Get only a user who is registered"""
        if not current_user.registered:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Kindly update your registration fees to access portal")
        return current_user
