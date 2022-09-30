from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from .. import schemas, models, utils, oauth2
from ..database import get_db


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=schemas.CreatedUser)
def get_current_user(
    current_user: str = Depends(oauth2.get_current_user), db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.delete("/")
def delete_user(
    current_user: str = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    user_query = db.query(models.User).filter(models.User.id == current_user.id)
    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found",
        )
    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CreatedUser,
)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
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
