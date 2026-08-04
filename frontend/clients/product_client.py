from core.api_client import request


def product_create(product: dict) -> dict:
    return request(
        "POST",
        "/product/create",
        json=product,
    )


def product_select_all() -> dict:
    return request(
        "GET",
        "/product/getall",
    )


def product_update(product_id: str, product: dict) -> dict:
    return request(
        "PUT",
        f"/product/{product_id}",
        json=product,
    )


def product_delete(product_id: str) -> dict:
    return request(
        "DELETE",
        f"/product/delete/{product_id}",
    )