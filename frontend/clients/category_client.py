from core.api_client import request


def category_create(name: str) -> dict:
    return request("POST", "/categories", json={"name": name})


def category_select_all() -> dict:
    return request("GET", "/categories")


def category_select(category_id: str) -> dict:
    return request("GET", f"/categories/{category_id}")


def category_update(category_id: str, name: str) -> dict:
    return request("PUT", f"/categories/{category_id}", json={"name": name})


def category_delete(category_id: str) -> dict:
    return request("DELETE", f"/categories/{category_id}")


def category_products(category_id: str) -> dict:
    return request("GET", f"/categories/{category_id}/products")
