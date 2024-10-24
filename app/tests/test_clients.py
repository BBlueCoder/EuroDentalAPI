import pytest
from fastapi import status
from starlette.testclient import TestClient

from app.utils.global_utils import global_prefix

CLIENTS_PATH = f"{global_prefix}/clients"
def test_get_all_clients(client: TestClient):
    res = client.get(CLIENTS_PATH)
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "email, client_id",
    [("test1@mail.com", 1), ("test2@mail.com", 1), ("test3@mail.com", 1)],
)
def test_create_client(client: TestClient, email, client_id):
    res = client.post(CLIENTS_PATH, data={"email": email})
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("id") == client_id


def test_create_and_get_clients(client: TestClient):
    client.post(CLIENTS_PATH, data={"email": "test@mail.com"})
    client.post(CLIENTS_PATH, data={"email": "test2@mail.com"})

    res = client.get(CLIENTS_PATH)
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == 2


def test_get_not_found_client_by_id(client: TestClient):
    res = client.get(f"{CLIENTS_PATH}/1")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_create_client_get_client_by_id(client: TestClient):
    client.post(CLIENTS_PATH, data={"email": "test@mail.com"})

    res = client.get(f"{CLIENTS_PATH}/1")
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("email") == "test@mail.com"


def test_create_client_without_email(client: TestClient):
    res = client.post(CLIENTS_PATH)
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "first_name, last_name",
    [
        ("name1", "lastname1"),
        ("name2", "lastname2"),
        ("name3", "lastname3"),
    ],
)
def test_update_client(client: TestClient, first_name, last_name):
    client_data = client.post(CLIENTS_PATH, data={"email": "test@mail.com"}).json()

    res = client.put(
        f"{CLIENTS_PATH}/{client_data["id"]}",
        data={"first_name": first_name, "last_name": last_name},
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("first_name") == first_name
    assert res.json().get("last_name") == last_name
    assert res.json().get("email") == "test@mail.com"


def test_update_client_email(client: TestClient):
    client_data = client.post(CLIENTS_PATH, data={"email": "test@mail.com"}).json()

    res = client.put(
        f"{CLIENTS_PATH}/{client_data["id"]}",
        data={"email": "update@mail.com"},
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("email") == "update@mail.com"


def test_update_invalid_client(client: TestClient):
    res = client.put(f"{CLIENTS_PATH}/1", data={"first_name": "test"})
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_delete_client(client: TestClient):
    client_data = client.post(CLIENTS_PATH, data={"email": "test@mail.com"}).json()

    res = client.delete(f"{CLIENTS_PATH}/{client_data["id"]}")
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_delete_invalid_client(client: TestClient):
    res = client.delete(f"{CLIENTS_PATH}/1")
    assert res.status_code == status.HTTP_404_NOT_FOUND
