import pytest
from fastapi import status
from starlette.testclient import TestClient

PROFILES_PATH = "/profiles"
profiles = [
    "profile1",
    "profile2",
    "profile3",
]


def test_get_all_profiles(client: TestClient):
    res = client.get(PROFILES_PATH)
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("profile", profiles)
def test_create_profiles(client: TestClient, profile: str):
    res = client.post(PROFILES_PATH, json={"profile_name": profile})
    assert res.status_code == status.HTTP_200_OK


def test_create_profile_without_value(client: TestClient):
    res = client.post(PROFILES_PATH)

    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_and_get_profiles(client: TestClient):
    for profile in profiles:
        client.post(PROFILES_PATH, json={"profile_name": profile})

    res = client.get(PROFILES_PATH)
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == len(profiles)


def test_get_profile_by_id(client: TestClient):
    profile_data = client.post(PROFILES_PATH, json={"profile_name": profiles[0]}).json()

    res = client.get(f"{PROFILES_PATH}/{profile_data["id"]}")
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["profile_name"] == profiles[0]


def test_get_invalid_profile_by_id(client: TestClient):
    res = client.get(f"{PROFILES_PATH}/0")
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "profile",
    [
        "profile5",
        "profile6",
        "profile7",
    ],
)
def test_update_profile(client: TestClient, profile: str):
    profile_data = client.post(PROFILES_PATH, json={"profile_name": profile}).json()

    res = client.put(
        f"{PROFILES_PATH}/{profile_data["id"]}", json={"profile_name": profile}
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.json()["profile_name"] == profile


def test_update_invalid_profile(client: TestClient):
    res = client.put(f"{PROFILES_PATH}/0", json={"profile_name": "profile_update"})

    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_update_profile_without_value(client: TestClient):
    res = client.put(f"{PROFILES_PATH}/1")

    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def delete_profile(client: TestClient):
    profile_data = client.post(PROFILES_PATH, json={"profile_name": profiles[0]}).json()

    res = client.delete(f"{PROFILES_PATH}/{profile_data["id"]}")

    assert res.status_code == status.HTTP_204_NO_CONTENT


def delete_invalid_profile(client: TestClient):
    res = client.delete(f"{PROFILES_PATH}/0")

    assert res.status_code == status.HTTP_404_NOT_FOUND
