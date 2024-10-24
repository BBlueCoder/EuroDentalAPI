import pytest
from fastapi import status
from starlette.testclient import TestClient

from app.models.profiles import Profile
from app.utils.global_utils import global_prefix

USERS_PATH = f"{global_prefix}/users"

@pytest.fixture(name="user")
def user_fixture(profile: Profile):
    return {"email": "user@mail.com", "profile_id": profile.id, "password": "password"}


def test_get_all_users(client: TestClient):
    res = client.get(USERS_PATH)
    assert res.status_code == status.HTTP_200_OK


def test_create_user(client: TestClient, user):
    res = client.post(USERS_PATH, data=user)
    assert res.status_code == status.HTTP_200_OK


def test_create_and_get_users(client: TestClient, user):
    client.post(USERS_PATH, data=user)

    res = client.get(USERS_PATH)
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == 1


def test_get_not_found_user_by_id(client: TestClient):
    res = client.get(f"{USERS_PATH}/1")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_create_user_get_user_by_id(client: TestClient, user):
    client.post(USERS_PATH, data=user)

    res = client.get(f"{USERS_PATH}/1")

    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("email") == user["email"]


def test_create_user_without_email(client: TestClient):
    res = client.post(USERS_PATH)
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_block_users(client : TestClient, user):
    client.post(USERS_PATH,data=user)

    res = client.get(f"{USERS_PATH}/1")

    assert res.status_code == status.HTTP_200_OK
    assert res.json()["is_blocked"] == False

    res = client.post(f"{USERS_PATH}/block_users",json={
        "user_ids":[
            1
        ],
        "block": 1==1
    })
    assert res.status_code == status.HTTP_200_OK

    res = client.get(f"{USERS_PATH}/1")

    assert res.status_code == status.HTTP_200_OK
    assert res.json()["is_blocked"] == True

@pytest.mark.parametrize(
    "first_name, last_name",
    [
        ("name1", "lastname1"),
        ("name2", "lastname2"),
        ("name3", "lastname3"),
    ],
)
def test_update_user(client: TestClient, first_name, last_name, user):
    user_data = client.post(USERS_PATH, data=user).json()

    res = client.put(
        f"{USERS_PATH}/{user_data["id"]}",
        data={"first_name": first_name, "last_name": last_name},
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("first_name") == first_name
    assert res.json().get("last_name") == last_name


def test_update_invalid_user(client: TestClient):
    res = client.put(f"{USERS_PATH}/1", data={"first_name": "test"})
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user(client: TestClient, user):
    user_data = client.post(USERS_PATH, data=user).json()

    res = client.delete(f"{USERS_PATH}/{user_data["id"]}")
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_delete_invalid_user(client: TestClient):
    res = client.delete(f"{USERS_PATH}/1")
    assert res.status_code == status.HTTP_404_NOT_FOUND
