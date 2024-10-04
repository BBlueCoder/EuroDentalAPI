import pytest
from fastapi import status
from sqlmodel import Session
from starlette.testclient import TestClient

from app.models.clients import Client
from app.models.tasks import Task
from app.models.users import User

TASKS_PATH = "/tasks"
tasks = [
    "task1",
    "task2",
    "task3",
]

@pytest.fixture(name="client_db")
def client_fixture(session : Session):
    client = Client(email="client@mail.com")
    session.add(client)
    session.commit()
    session.refresh(client)
    return client

@pytest.fixture(name="task")
def task_fixture(client_db : Client, user_db : User):
    return {"task_name": "task1", "client_id" : client_db.id, "create_by":user_db.id, "status":"working"}

def test_get_all_tasks(client: TestClient):
    res = client.get(TASKS_PATH)
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("task_name", tasks)
def test_create_tasks(client: TestClient, task_name: str, task):
    task["task_name"] = task_name
    res = client.post(TASKS_PATH, json=task)
    assert res.status_code == status.HTTP_200_OK


def test_create_task_without_value(client: TestClient):
    res = client.post(TASKS_PATH)

    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_and_get_tasks(client: TestClient,task):
    for task_name in tasks:
        task["task_name"] = task_name
        client.post(TASKS_PATH, json=task)

    res = client.get(TASKS_PATH)
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == len(tasks)


def test_get_task_by_id(client: TestClient, task):
    task_data = client.post(
        TASKS_PATH, json=task
    ).json()

    res = client.get(f"{TASKS_PATH}/{task_data["id"]}")
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["task_name"] == tasks[0]


def test_get_invalid_task_by_id(client: TestClient):
    res = client.get(f"{TASKS_PATH}/0")
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "task_name",
    [
        "task5",
        "task6",
        "task7",
    ],
)
def test_update_task(client: TestClient, task_name: str, task):
    task_data = client.post(TASKS_PATH, json=task).json()

    res = client.put(
        f"{TASKS_PATH}/{task_data["id"]}", json={"task_name": task_name}
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.json()["task_name"] == task_name


def test_update_invalid_task(client: TestClient, task):
    res = client.put(f"{TASKS_PATH}/0", json={"task_name": "task1"})

    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_update_task_without_value(client: TestClient):
    res = client.put(f"{TASKS_PATH}/1")

    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def delete_task(client: TestClient, task):
    task_data = client.post(
        TASKS_PATH, json=task
    ).json()

    res = client.delete(f"{TASKS_PATH}/{task_data["id"]}")

    assert res.status_code == status.HTTP_204_NO_CONTENT


def delete_invalid_task(client: TestClient):
    res = client.delete(f"{TASKS_PATH}/0")

    assert res.status_code == status.HTTP_404_NOT_FOUND
