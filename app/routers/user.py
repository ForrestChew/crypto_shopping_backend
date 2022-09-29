from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from .. import schemas, models, utils, oauth2
from ..database import get_db


router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.CreatedUser
)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.delete("/{id}")
def delete_user(
    id: int,
    current_user: str = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    print("Queried ID", id)
    print("User ID", user.id)
    print("Current User ID", current_user.id)
    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
