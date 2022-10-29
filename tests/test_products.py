from app import schemas
from fastapi import status
import pytest


@pytest.mark.parametrize(
    "title, category, description, price, quantity, image_title, is_top_deal",
    [
        (
            "Baking Sheet set | 10 Piece Pack",
            "Cooking",
            "This description",
            "25.99",
            "10",
            "red-vines-candy.png",
            "false",
        ),
        (
            "Harry Potter Series | Hard Cover",
            "Books",
            "test description",
            "15.99",
            "5",
            "red-vines-candy.png",
            "true",
        ),
        (
            "Acer Aspire-1550 Computer",
            "Electronics",
            "another",
            "900.00",
            "25",
            "red-vines-candy.png",
            "true",
        ),
    ],
)
def test_create_product(
    authed_client_admin,
    title,
    category,
    description,
    price,
    quantity,
    image_title,
    is_top_deal,
):
    res = authed_client_admin.post(
        "/products/",
        json={
            "title": title,
            "category": category,
            "description": description,
            "price": float(price),
            "quantity": int(quantity),
            "image_title": image_title,
            "is_top_deal": is_top_deal,
        },
    )
    new_product = schemas.ProductOut(**res.json())

    assert res.status_code == 201
    assert new_product.title == title.lower()
    assert new_product.category == category.lower()
    assert new_product.description == description
    assert new_product.price == float(price)
    assert new_product.quantity == int(quantity)


@pytest.mark.parametrize(
    "title, category, description, price, quantity, image_title, is_top_deal",
    [
        (
            "Cards",
            "Entertainment",
            "this description",
            "4.99",
            "100",
            "test.png",
            "false",
        ),
        (
            "Dark Tower",
            "Books",
            "this description",
            "90.00",
            "2",
            "test-image.png",
            "true",
        ),
        (
            "50inch Flat Screen TV",
            "Electronics",
            "description",
            "750.00",
            "8",
            "cool-cats.png",
            "false",
        ),
    ],
)
def test_create_product_unauthorized(
    client, title, category, description, price, quantity, image_title, is_top_deal
):
    res = client.post(
        "/products/",
        json={
            "title": title,
            "category": category,
            "description": description,
            "price": float(price),
            "quantity": int(quantity),
            "image_title": image_title,
            "is_top_deal": is_top_deal,
        },
    )
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_products(client, create_multiple_products):
    res = client.get("/products/")
    products = res.json()
    assert res.status_code == status.HTTP_200_OK
    assert len(products) == 9


@pytest.mark.parametrize(
    "product_id",
    [(1), (2), (3), (4), (5), (6), (7), (8), (9)],
)
def test_get_product_by_id(client, create_multiple_products, product_id):
    res = client.get(f"/products/{product_id}")
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "title",
    [
        ("Printer"),
        ("point brushes"),
        ("printer paper"),
        ("pens"),
        ("midi"),
        ("tv"),
        ("leather jacket"),
    ],
)
def test_get_product_by_title(client, create_multiple_products, title):
    res = client.get(f"/products?search={title}")
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("search", [("Leather"), ("pens"), ("midi")])
def test_get_search_results(client, create_multiple_products, search):
    res = client.get(f"/products/product-search?search={search}")
    assert res.status_code == status.HTTP_200_OK
