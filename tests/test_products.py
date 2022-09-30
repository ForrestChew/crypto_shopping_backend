from app import schemas
import pytest


@pytest.mark.parametrize(
    "title, category, price, quantity",
    [
        ("Baking Sheet set | 10 Piece Pack", "Cooking", "25.99", "10"),
        ("Harry Potter Series | Hard Cover", "Books", "15.99", "5"),
        ("Acer Aspire-1550 Computer", "Electronics", "900", "25"),
    ],
)
def test_create_product(authed_admin_client, title, category, price, quantity):
    res = authed_admin_client.post(
        "/products/",
        json={
            "title": title,
            "category": category,
            "price": float(price),
            "quantity": int(quantity),
        },
    )
    new_product = schemas.CreatedProduct(**res.json())
    assert res.status_code == 201
    assert new_product.title == title
    assert new_product.category == category.lower()
    assert new_product.price == float(price)
    assert new_product.quantity == int(quantity)


@pytest.mark.parametrize(
    "title, category, price, quantity",
    [
        ("Cards", "Entertainment", "4.99", "100"),
        ("Dark Tower", "Books", "90.00", "2"),
        ("50inch Flat Screen TV", "Electronics", "750.00", "8"),
    ],
)
def test_create_product_authorized_non_admin(
    authed_client, title, category, price, quantity
):
    res = authed_client.post(
        "/products/",
        json={
            "title": title,
            "category": category,
            "price": float(price),
            "quantity": int(quantity),
        },
    )
    assert res.status_code == 403


@pytest.mark.parametrize(
    "title, category, price, quantity",
    [
        ("Lego Castle", "Toys", "50", "20"),
        ("HDMI Cable", "Electronics", "12.99", "2"),
        ("Stuffed animal Lizard", "Toys", "20.99", "15"),
    ],
)
def test_create_product_unauthorized(client, title, category, price, quantity):
    res = client.post(
        "/products/",
        json={
            "title": title,
            "category": category,
            "price": float(price),
            "quantity": int(quantity),
        },
    )
    assert res.status_code == 401


@pytest.mark.parametrize(
    "product_id",
    [(1), (2), (3), (4), (5), (6), (7), (8), (9), (10)],
)
def test_get_product_by_id(client, create_multiple_products, product_id):
    res = client.get(f"/products/{product_id}")
    assert res.status_code == 200


@pytest.mark.parametrize(
    "category",
    [
        ("electronics"),
        ("arts and crafts"),
        ("office supplies"),
        ("musical instruments"),
        ("clothing"),
        ("home goods"),
        ("Accessories"),
    ],
)
def test_get_product_by_category(client, create_multiple_products, category):
    res = client.get(f"/products?search={category}")
    assert res.status_code == 200
