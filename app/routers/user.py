from fastapi import status, HTTPException, Depends, APIRouter, Response
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from .. import schemas, models, utils
from ..database import get_db


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    if not current_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    current_user = (
        db.query(models.User).filter(models.User.id == current_user_id).first()
    )
    return current_user


@router.delete("/")
def delete_user(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user_query = db.query(models.User).filter(models.User.id == current_user_id)
    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/",
    response_model=schemas.UserOut,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    new_cart = models.Cart(**{"user_id": new_user.id})
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return new_user
