import pytest
from fastapi import status
from starlette.testclient import TestClient

from app.utils.global_utils import global_prefix

BRANDS_PATH = f"{global_prefix}/brands"
brands = [
    "brand1",
    "brand2",
    "brand3",
]


def test_get_all_brands(client: TestClient):
    res = client.get(BRANDS_PATH)
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("brand", brands)
def test_create_brands(client: TestClient, brand: str):
    res = client.post(BRANDS_PATH, json={"brand": brand})
    assert res.status_code == status.HTTP_200_OK


def test_create_brand_without_value(client: TestClient):
    res = client.post(BRANDS_PATH)

    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_and_get_brands(client: TestClient):
    for brand in brands:
        client.post(BRANDS_PATH, json={"brand": brand})

    res = client.get(BRANDS_PATH)
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == len(brands)


def test_get_brand_by_id(client: TestClient):
    brand_data = client.post(BRANDS_PATH, json={"brand": brands[0]}).json()

    res = client.get(f"{BRANDS_PATH}/{brand_data["id"]}")
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["brand"] == brands[0]


def test_get_invalid_brand_by_id(client: TestClient):
    res = client.get(f"{BRANDS_PATH}/0")
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "brand",
    [
        "brand5",
        "brand6",
        "brand7",
    ],
)
def test_update_brand(client: TestClient, brand: str):
    brand_data = client.post(BRANDS_PATH, json={"brand": brand}).json()

    res = client.put(f"{BRANDS_PATH}/{brand_data["id"]}", json={"brand": brand})

    assert res.status_code == status.HTTP_200_OK
    assert res.json()["brand"] == brand


def test_update_invalid_brand(client: TestClient):
    res = client.put(f"{BRANDS_PATH}/0", json={"brand": "brand_update"})

    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_update_brand_without_value(client: TestClient):
    res = client.put(f"{BRANDS_PATH}/1")

    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def delete_brand(client: TestClient):
    brand_data = client.post(BRANDS_PATH, json={"brand": brands[0]}).json()

    res = client.delete(f"{BRANDS_PATH}/{brand_data["id"]}")

    assert res.status_code == status.HTTP_204_NO_CONTENT


def delete_invalid_brand(client: TestClient):
    res = client.delete(f"{BRANDS_PATH}/0")

    assert res.status_code == status.HTTP_404_NOT_FOUND
