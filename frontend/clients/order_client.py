from core.api_client import request


def order_create(order: dict) -> dict:
    return request("POST", "/order/create", json=order)


def order_list(customer_id: str) -> dict:
    return request("GET", f"/order/list/{customer_id}")


def order_get(order_id: str) -> dict:
    return request("GET", f"/order/get/{order_id}")


def order_update_status(order_id: str, status: str) -> dict:
    return request("PATCH", f"/order/{order_id}/status", json={"status": status})


def order_cancel(order_id: str) -> dict:
    return request("POST", f"/order/{order_id}/cancel")


def order_delete(order_id: str) -> dict:
    return request("DELETE", f"/order/{order_id}")
