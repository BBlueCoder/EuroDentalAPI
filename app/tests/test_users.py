import pytest
from fastapi import status
from starlette.testclient import TestClient

from app.models.profiles import Profile

@pytest.fixture(name="user")
def user_fixture(profile : Profile):
    return {"email": "user@mail.com", "profile_id":profile.id, "password": "password"}

def test_get_all_users(client: TestClient):
    res = client.get("/users")
    assert res.status_code == status.HTTP_200_OK


def test_create_user(client: TestClient, user):
    res = client.post("/users", data=user)
    assert res.status_code == status.HTTP_200_OK

def test_create_and_get_users(client: TestClient, user):
    client.post("/users", data=user)

    res = client.get("/users")
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == 1


def test_get_not_found_user_by_id(client: TestClient):
    res = client.get("/users/1")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_create_user_get_user_by_id(client: TestClient,user):
    client.post("/users", data=user)

    res = client.get("/users/1")
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("email") == user["email"]


def test_create_user_without_email(client: TestClient):
    res = client.post("/users")
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "first_name, last_name",
    [
        ("name1", "lastname1"),
        ("name2", "lastname2"),
        ("name3", "lastname3"),
    ],
)
def test_update_user(client: TestClient, first_name, last_name, user):
    user_data = client.post("/users", data=user).json()

    res = client.put(
        f"/users/{user_data["id"]}",
        data={"first_name": first_name, "last_name": last_name},
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("first_name") == first_name
    assert res.json().get("last_name") == last_name


def test_update_invalid_user(client: TestClient):
    res = client.put("/users/1", data={"first_name": "test"})
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user(client: TestClient, user):
    user_data = client.post("/users", data=user).json()

    res = client.delete(f"/users/{user_data["id"]}")
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_delete_invalid_user(client: TestClient):
    res = client.delete("/users/1")
    assert res.status_code == status.HTTP_404_NOT_FOUND
