from .database import Base
from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    Boolean,
    TIMESTAMP,
)
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_administrator = Column(Boolean, server_default="False")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Integer, server_default="0")
    quantity = Column(Integer, nullable=False)
    is_top_deal = Column(Boolean, server_default="False")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

    product_image_path = relationship("ProductImagePath")


class ProductImagePath(Base):
    __tablename__ = "product_image_paths"

    id = Column(Integer, primary_key=True, nullable=False)
    image_path = Column(String, nullable=False)
    product_id = Column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    cart_quantity = Column(Integer, server_default="0")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

    user = relationship("User")


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, nullable=False)
    cart_id = Column(
        Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False
    )
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    cart = relationship("Cart")
    product = relationship("Product")
