from ... import schemas, models


def get_valid_new_product_info_for_db(product: schemas.ProductIn):
    """Extracts the image path from the input product schema to be
    saved in the product_image_paths table in Postgres. Also converts
    fields into lowercase."""
    product_dict = product.dict()
    product_dict["title"] = product_dict["title"].lower()
    product_dict["category"] = product_dict["category"].lower()
    image_path = product_dict.pop("image_path")
    new_product = models.Product(**product_dict)
    return new_product, image_path
