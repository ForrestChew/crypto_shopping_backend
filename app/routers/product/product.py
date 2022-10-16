from symbol import test_nocond
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi_jwt_auth import AuthJWT
from typing import List, Optional
from ... import models, schemas
from sqlalchemy.orm import Session
from ...database import get_db
from .utils import get_valid_new_product_info_for_db


router = APIRouter(prefix="/products", tags=["Products"])


@router.get(
    "/", response_model=List[schemas.ProductOut], status_code=status.HTTP_200_OK
)
def get_products(
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
    db: Session = Depends(get_db),
):
    products = (
        db.query(
            models.Product.id,
            models.Product.title,
            models.Product.price,
            models.Product.quantity,
            models.Product.category,
            models.Product.rating,
            models.ProductImagePath.image_path,
        )
        .outerjoin(
            models.ProductImagePath,
            models.Product.id == models.ProductImagePath.product_id,
        )
        .filter(models.Product.category.contains(search.lower()))
        .limit(limit)
        .offset(skip)
    ).all()
    return products


@router.get("/{id}", response_model=schemas.ProductOut, status_code=status.HTTP_200_OK)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    return product


@router.post(
    "/", response_model=schemas.ProductOut, status_code=status.HTTP_201_CREATED
)
def create_product(
    product: schemas.ProductIn,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    current_user = (
        db.query(models.User).filter(models.User.id == current_user_id).first()
    )
    if not current_user.is_administrator:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not administrator"
        )
    new_product, image_path = get_valid_new_product_info_for_db(product)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    new_image_path = models.ProductImagePath(
        **{"image_path": image_path, "product_id": new_product.id}
    )
    db.add(new_image_path)
    db.commit()
    db.refresh(new_image_path)
    return new_product
