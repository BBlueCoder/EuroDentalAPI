from starlette.testclient import TestClient
from fastapi import status
import pytest

CATEGORIES_PATH = "/categories"
categories = [
    "category1",
    "category2",
    "category3",
]

def test_get_all_categories(client: TestClient):
    res = client.get(CATEGORIES_PATH)
    assert res.status_code == status.HTTP_200_OK

@pytest.mark.parametrize("category", categories)
def test_create_categories(client: TestClient, category: str):
    res = client.post(CATEGORIES_PATH, json={"category":category})
    assert res.status_code == status.HTTP_200_OK

def test_create_category_without_value(client: TestClient):
    res = client.post(CATEGORIES_PATH)

    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_and_get_categories(client: TestClient):
    for category in categories:
        client.post(CATEGORIES_PATH, json={"category":category})

    res = client.get(CATEGORIES_PATH)
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == len(categories)

def test_get_category_by_id(client: TestClient):
    category_data = client.post(CATEGORIES_PATH, json={"category": categories[0]}).json()

    res = client.get(f"{CATEGORIES_PATH}/{category_data["id"]}")
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["category"] == categories[0]

def test_get_invalid_category_by_id(client: TestClient):
    res = client.get(f"{CATEGORIES_PATH}/0")
    assert res.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.parametrize("category", [
    "category5",
    "category6",
    "category7",
])
def test_update_category(client: TestClient, category : str):
    category_data = client.post(CATEGORIES_PATH, json={"category": category}).json()

    res = client.put(f"{CATEGORIES_PATH}/{category_data["id"]}", json={"category":category})

    assert res.status_code == status.HTTP_200_OK
    assert res.json()["category"] == category

def test_update_invalid_category(client: TestClient):
    res = client.put(f"{CATEGORIES_PATH}/0", json={"category":"category_update"})

    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_update_category_without_value(client: TestClient):
    res = client.put(f"{CATEGORIES_PATH}/1")

    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def delete_category(client: TestClient):
    category_data = client.post(CATEGORIES_PATH, json={"category": categories[0]}).json()

    res = client.delete(f"{CATEGORIES_PATH}/{category_data["id"]}")

    assert res.status_code == status.HTTP_204_NO_CONTENT

def delete_invalid_category(client: TestClient):
    res = client.delete(f"{CATEGORIES_PATH}/0")

    assert res.status_code == status.HTTP_404_NOT_FOUND

