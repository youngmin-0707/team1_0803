from core.api_client import request


def review_create(review: dict) -> dict:
    return request(
        "POST",
        "/review/create",
        json=review,
    )


def review_getall(product_id: str) -> dict:
    return request(
        "GET",
        f"/review/product/{product_id}",
    )


def review_update(review_id: str, review: dict) -> dict:
    return request(
        "PUT",
        f"/review/{review_id}",
        json=review,
    )


def review_delete(review_id: str, customer_id: str) -> dict:
    return request(
        "DELETE",
        f"/review/{review_id}",
        json={
            "customer_id": customer_id,
        },
    )
