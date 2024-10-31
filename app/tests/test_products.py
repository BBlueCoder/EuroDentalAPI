import pytest
from fastapi import status
from starlette.testclient import TestClient

from app.utils.global_utils import global_prefix

PRODUCTS_PATH = f"{global_prefix}/products"

def test_get_all_products(client: TestClient):
    res = client.get(PRODUCTS_PATH)
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "product_name, ref",
    [("product1", "ref001"), ("product2", "ref002"), ("product3", "ref003")],
)
def test_create_product(client: TestClient, product_name, ref):
    res = client.post(
        PRODUCTS_PATH, data={"product_name": product_name, "reference": ref}
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("product_name") == product_name


# def test_create_and_get_products(client: TestClient):
#     client.post(PRODUCTS_PATH, data={"product_name": "product1", "reference": "ref001"})
#     client.post(PRODUCTS_PATH, data={"product_name": "product2", "reference": "ref002"})

#     res = client.get(PRODUCTS_PATH)
#     assert res.status_code == status.HTTP_200_OK
#     assert len(res.json()) == 2


def test_get_not_found_product_by_id(client: TestClient):
    res = client.get(f"{PRODUCTS_PATH}/1")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_create_product_get_product_by_id(client: TestClient):
    client.post(PRODUCTS_PATH, data={"product_name": "product1", "reference": "ref001"})

    res = client.get(f"{PRODUCTS_PATH}/1")
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("product_name") == "product1"


def test_create_product_without_product_name(client: TestClient):
    res = client.post(PRODUCTS_PATH, data={"reference": "ref001"})
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "product_name",
    ["product1", "product2", "product3"],
)
def test_update_product(client: TestClient, product_name):
    product_data = client.post(
        PRODUCTS_PATH,
        data={"product_name": "product", "reference": "ref001", "price": 33.5},
    ).json()

    res = client.put(
        f"{PRODUCTS_PATH}/{product_data["id"]}",
        data={"product_name": product_name},
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("product_name") == product_name
    assert res.json().get("price") == 33.5

def test_update_products_quantity(client : TestClient):
    product_data_1 = client.post(
        PRODUCTS_PATH,
        data={"product_name": "product", "reference": "ref001", "price": 33.5},
    ).json()
    product_data_2 = client.post(
        PRODUCTS_PATH,
        data={"product_name": "product2", "reference": "ref002", "stock_quantity":5},
    ).json()

    data = [
        {"reference":product_data_1["reference"],"stock_quantity":3},
        {"reference": product_data_2["reference"], "stock_quantity": 6}
    ]
    client.put(f"{PRODUCTS_PATH}/quantity",json=data)

    res = client.get(f"{PRODUCTS_PATH}/{product_data_1["id"]}")
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["stock_quantity"] == 3
    res = client.get(f"{PRODUCTS_PATH}/{product_data_2["id"]}")
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["stock_quantity"] == 11


def test_update_invalid_product(client: TestClient):
    res = client.put(f"{PRODUCTS_PATH}/1", data={"product_name": "test"})
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_delete_product(client: TestClient):
    product_data = client.post(
        PRODUCTS_PATH, data={"product_name": "product1", "reference": "ref001"}
    ).json()

    res = client.delete(f"{PRODUCTS_PATH}/{product_data["id"]}")
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_delete_invalid_product(client: TestClient):
    res = client.delete(f"{PRODUCTS_PATH}/1")
    assert res.status_code == status.HTTP_404_NOT_FOUND
