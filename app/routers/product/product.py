from unicodedata import name
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.responses import FileResponse
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
    search: Optional[str] = "",
    db: Session = Depends(get_db),
):
    products = (
        db.query(
            models.Product.id,
            models.Product.title,
            models.Product.price,
            models.Product.quantity,
            models.Product.description,
            models.Product.category,
            models.Product.is_top_deal,
            models.ProductImageTitle.image_title,
        )
        .outerjoin(
            models.ProductImageTitle,
            models.Product.id == models.ProductImageTitle.product_id,
        )
        .filter(models.Product.title.contains(search.lower()))
    ).all()
    return products


@router.get(
    "/category/{category}",
    response_model=List[schemas.ProductOut],
    status_code=status.HTTP_200_OK,
)
def get_products_by_category(category: str, db: Session = Depends(get_db)):
    products = (
        db.query(
            models.Product.id,
            models.Product.title,
            models.Product.price,
            models.Product.quantity,
            models.Product.description,
            models.Product.category,
            models.Product.is_top_deal,
            models.ProductImageTitle.image_title,
        )
        .outerjoin(
            models.ProductImageTitle,
            models.Product.id == models.ProductImageTitle.product_id,
        )
        .filter(models.Product.category == category)
    ).all()
    return products


@router.get("/images/{img_title}", status_code=status.HTTP_200_OK)
def get_image(img_title: str):
    relative_path = f"product_images/{img_title}"
    return FileResponse(relative_path)


@router.get(
    "/top-deals",
    response_model=List[schemas.ProductOut],
    status_code=status.HTTP_200_OK,
)
def get_top_deals(db: Session = Depends(get_db), limit: int = 8, skip: int = 0):
    products = (
        db.query(
            models.Product.id,
            models.Product.title,
            models.Product.price,
            models.Product.quantity,
            models.Product.description,
            models.Product.category,
            models.Product.is_top_deal,
            models.ProductImageTitle.image_title,
        )
        .outerjoin(
            models.ProductImageTitle,
            models.Product.id == models.ProductImageTitle.product_id,
        )
        .filter(models.Product.is_top_deal == True)
        .offset(skip)
        .limit(limit)
    ).all()
    return products


@router.get(
    "/product-search",
    response_model=List[schemas.SearchResults],
    status_code=status.HTTP_200_OK,
)
def get_search_results(search: Optional[str] = "", db: Session = Depends(get_db)):
    search_results = (
        db.query(models.Product.id, models.Product.title, models.Product.category)
        .filter(models.Product.title.contains(search))
        .limit(8)
        .all()
    )
    return search_results


@router.get("/{id}", response_model=schemas.ProductOut, status_code=status.HTTP_200_OK)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = (
        db.query(
            models.Product.id,
            models.Product.title,
            models.Product.price,
            models.Product.quantity,
            models.Product.description,
            models.Product.category,
            models.Product.is_top_deal,
            models.ProductImageTitle.image_title,
        )
        .outerjoin(
            models.ProductImageTitle,
            models.Product.id == models.ProductImageTitle.product_id,
        )
        .filter(models.Product.id == id)
    ).first()
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
    new_product, image_title = get_valid_new_product_info_for_db(product)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    image_title = models.ProductImageTitle(
        **{"image_title": image_title, "product_id": new_product.id}
    )
    db.add(image_title)
    db.commit()
    db.refresh(image_title)
    return new_product
