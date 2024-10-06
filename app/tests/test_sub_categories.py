import pytest
from fastapi import status
from starlette.testclient import TestClient

from app.models.categories import CategoryRead

SUB_CATEGORIES_PATH = "/sub_categories"


@pytest.fixture(name="categories")
def categories_fixture(client: TestClient):
    client.post("/categories", json={"category": "category1"})
    client.post("/categories", json={"category": "category2"})

    res = client.get("/categories")
    categories = [CategoryRead(**category) for category in res.json()]

    return categories


@pytest.fixture(name="sub_categories")
def sub_categories_fixture(categories: list[CategoryRead]):
    sub_categories = []
    for i, category in enumerate(categories):
        sub_categories.append(
            {"sub_category": f"sub_category{i+1}", "category_id": category.id}
        )

    return sub_categories


def test_get_all_sub_categories(client: TestClient):
    res = client.get(SUB_CATEGORIES_PATH)

    assert res.status_code == status.HTTP_200_OK


def test_create_sub_category(client: TestClient, sub_categories):
    res = client.post(
        SUB_CATEGORIES_PATH,
        json={
            "sub_category": sub_categories[0]["sub_category"],
            "category_id": sub_categories[0]["category_id"],
        },
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("sub_category") == sub_categories[0]["sub_category"]


def test_create_sub_category_with_invalid_data(client: TestClient):
    res = client.post(SUB_CATEGORIES_PATH)

    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_sub_category_by_id(client: TestClient, sub_categories):
    sub_category_data = client.post(
        SUB_CATEGORIES_PATH,
        json={
            "sub_category": sub_categories[0]["sub_category"],
            "category_id": sub_categories[0]["category_id"],
        },
    ).json()

    res = client.get(f"{SUB_CATEGORIES_PATH}/{sub_category_data["id"]}")

    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("sub_category") == sub_categories[0]["sub_category"]


@pytest.mark.parametrize("sub_category_id", ["5"])
def test_get_sub_category_with_invalid_id(client: TestClient, sub_category_id):
    res = client.get(f"{SUB_CATEGORIES_PATH}/{sub_category_id}")

    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "category_id, res_len",
    [
        (1, 1),
        (2, 1),
        (0, 2),
    ],
)
def test_create_and_get_sub_categories(
    client: TestClient, sub_categories, category_id, res_len
):
    client.post(
        SUB_CATEGORIES_PATH,
        json={
            "sub_category": sub_categories[0]["sub_category"],
            "category_id": sub_categories[0]["category_id"],
        },
    )
    client.post(
        SUB_CATEGORIES_PATH,
        json={
            "sub_category": sub_categories[1]["sub_category"],
            "category_id": sub_categories[1]["category_id"],
        },
    )
    if category_id:
        res = client.get(f"{SUB_CATEGORIES_PATH}?category_id={category_id}")
    else:
        res = client.get(SUB_CATEGORIES_PATH)

    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == res_len


def test_update_sub_category(client: TestClient, sub_categories):
    sub_category_data = client.post(
        SUB_CATEGORIES_PATH,
        json={
            "sub_category": sub_categories[0]["sub_category"],
            "category_id": sub_categories[0]["category_id"],
        },
    ).json()

    res = client.put(
        f"{SUB_CATEGORIES_PATH}/{sub_category_data["id"]}",
        json={"sub_category": "update"},
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["category_id"] == sub_categories[0]["category_id"]
    assert res.json()["sub_category"] == "update"


def test_update_invalid_sub_category(client: TestClient):
    res = client.put(f"{SUB_CATEGORIES_PATH}/5", json={"sub_category": "update"})
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_delete_sub_category(client: TestClient, sub_categories):
    sub_category_data = client.post(
        SUB_CATEGORIES_PATH,
        json={
            "sub_category": sub_categories[0]["sub_category"],
            "category_id": sub_categories[0]["category_id"],
        },
    ).json()

    res = client.delete(f"{SUB_CATEGORIES_PATH}/{sub_category_data["id"]}")

    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_delete_invalid_sub_category(client: TestClient):
    res = client.delete(f"{SUB_CATEGORIES_PATH}/5")

    assert res.status_code == status.HTTP_404_NOT_FOUND
