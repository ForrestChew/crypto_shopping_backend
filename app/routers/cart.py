from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db

router = APIRouter(prefix="/carts", tags=["Carts"])


@router.get("/{id}", response_model=schemas.CartOut, status_code=status.HTTP_200_OK)
def get_cart_by_id(id: int, db: Session = Depends(get_db)):
    cart = db.query(models.Cart).filter(models.Cart.id == str(id)).first()
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )
    return cart
