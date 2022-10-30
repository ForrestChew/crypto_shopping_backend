from passlib.context import CryptContext
from fastapi import Depends, status, HTTPException
from fastapi_jwt_auth import AuthJWT
from requests import Session
from app import models, database

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return password_context.hash(password)


def verify_password(non_hashed_password: str, hashed_password: str):
    return password_context.verify(non_hashed_password, hashed_password)


def verify_jwt_access_token(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Non-existant access token.",
        )


def get_user_id_from_jwt_access_token(
    Authorize: AuthJWT = Depends(),
):
    current_user_id = Authorize.get_jwt_subject()
    return str(current_user_id)
