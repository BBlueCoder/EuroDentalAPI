import pytest
from fastapi import status
from starlette.testclient import TestClient


def test_get_all_products(client: TestClient):
    res = client.get("/products")
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "product_name, ref",
    [("product1","ref001"), ("product2","ref002"),("product3", "ref003")],
)
def test_create_product(client: TestClient, product_name,ref):
    res = client.post("/products", data={"product_name": product_name, "reference":ref})
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("product_name") == product_name


def test_create_and_get_products(client: TestClient):
    client.post("/products", data={"product_name": "product1", "reference":"ref001"})
    client.post("/products", data={"product_name": "product2", "reference":"ref002"})

    res = client.get("/products")
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == 2


def test_get_not_found_product_by_id(client: TestClient):
    res = client.get("/products/1")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_create_product_get_product_by_id(client: TestClient):
    client.post("/products", data={"product_name": "product1", "reference":"ref001"})

    res = client.get("/products/1")
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("product_name") == "product1"


def test_create_product_without_product_name(client: TestClient):
    res = client.post("/products",data={"reference":"ref001"})
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "product_name",
    ["product1", "product2","product3"],
)
def test_update_product(client: TestClient, product_name):
    product_data = client.post("/products", data={"product_name": "product", "reference":"ref001","price":33.5}).json()

    res = client.put(
        f"/products/{product_data["id"]}",
        data={"product_name": product_name},
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("product_name") == product_name
    assert res.json().get("price") == 33.5

def test_update_invalid_product(client: TestClient):
    res = client.put("/products/1", data={"product_name": "test"})
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_delete_product(client: TestClient):
    product_data = client.post("/products", data={"product_name": "product1","reference":"ref001"}).json()

    res = client.delete(f"/products/{product_data["id"]}")
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_delete_invalid_product(client: TestClient):
    res = client.delete("/products/1")
    assert res.status_code == status.HTTP_404_NOT_FOUND
