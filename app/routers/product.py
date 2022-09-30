from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "/", response_model=schemas.CreatedProduct, status_code=status.HTTP_201_CREATED
)
def create_product(
    product: schemas.CreateProduct,
    current_user: str = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.is_administrator:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not administrator"
        )
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
