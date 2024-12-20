import pytest
from fastapi import status
from starlette.testclient import TestClient

from app.models.clients import Client
from app.models.products import Product
from app.models.users import User
from app.tests.test_task_products import TASK_PRODUCTS_PATH
from app.utils.global_utils import global_prefix

TASKS_PATH = f"{global_prefix}/tasks"
tasks = [
    "task1",
    "task2",
    "task3",
]

task_dates = ["2024-10-06", "2024-08-02", "2024-09-05"]


@pytest.fixture(name="task")
def task_fixture(client_db: Client, user_db: User):
    return {
        "task_name": "task1",
        "client_id": client_db.id,
        "create_by": user_db.id,
        "status":"In Progress"
    }


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


def test_create_task_with_task_product(client: TestClient, task, product: Product):
    task["task_name"] = "task1"
    task_data = client.post(TASKS_PATH, json=task).json()
    assert task_data

    client.post(
        TASK_PRODUCTS_PATH,
        json={"product_reference": product.reference, "task_id": task_data["id"]},
    )
    res = client.get(f"{TASKS_PATH}/{task_data["id"]}")
    assert res.status_code == status.HTTP_200_OK
    # assert res.json()["id_category"] == product.id_category

# def test_task_details(client: TestClient, task, product: Product):
#     task["task_name"] = "task1"
#     task_data = client.post(TASKS_PATH, json=task).json()
#     assert task_data

#     client.post(
#         TASK_PRODUCTS_PATH,
#         json={"product_reference": product.reference, "task_id": task_data["id"]},
#     )
#     res = client.get(f"{TASKS_PATH}/task_details/{task_data["id"]}")
#     assert res.status_code == status.HTTP_200_OK
#     assert len(res.json()["products"]) == 1


def test_create_and_get_tasks(client: TestClient, task):
    for task_name in tasks:
        task["task_name"] = task_name
        client.post(TASKS_PATH, json=task)

    res = client.get(TASKS_PATH)
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == len(tasks)


@pytest.fixture(name="save_tasks")
def save_tasks_fixture(client: TestClient, task: dict):
    for idx, task_name in enumerate(tasks):
        task["task_name"] = task_name
        task["task_date"] = task_dates[idx]
        client.post(TASKS_PATH, json=task)

    return ""

def test_assign_tasks_to_technician(client : TestClient, user_db, save_tasks):
    res = client.post(f"{TASKS_PATH}/assign_tasks",json={
        "task_ids":[
            1,
            2,
            3
        ],
        "technician_id":user_db.id
    })

    assert res.status_code == status.HTTP_200_OK
    for idx, task_name in enumerate(tasks):
        res = client.get(f"{TASKS_PATH}/{idx+1}")
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["technician_id"] == user_db.id


def test_get_tasks_sorted_by_date_desc(client: TestClient, save_tasks):
    res = client.get(TASKS_PATH)
    task_dates.sort(reverse=True)
    assert res.status_code == status.HTTP_200_OK
    assert res.json()[0]["task_date"] == task_dates[0]


def test_get_tasks_sorted_by_date_asc(client: TestClient, save_tasks):
    res = client.get(f"{TASKS_PATH}/?sort=asc")
    task_dates.sort()
    assert res.status_code == status.HTTP_200_OK
    assert res.json()[0]["task_date"] == task_dates[0]


def test_get_tasks_sorted_by_exact_date(client: TestClient, save_tasks):
    res = client.get(f"{TASKS_PATH}/?exact_date={task_dates[0]}")
    print(res.json())
    assert res.status_code == status.HTTP_200_OK
    assert res.json()[0]["task_date"] == task_dates[0]

    res = client.get(f"{TASKS_PATH}?exact_date=2023-05-02")
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == 0


def test_get_tasks_sorted_by_range_date(client: TestClient, save_tasks):
    task_dates.sort()
    res = client.get(
        f"{TASKS_PATH}/?date_range_start={task_dates[0]}&date_range_end={task_dates[len(task_dates)-1]}"
    )
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == len(task_dates)

    res = client.get(
        f"{TASKS_PATH}/?date_range_start={task_dates[0]}&date_range_end={task_dates[1]}"
    )
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == 2


def test_get_task_by_id(client: TestClient, task):
    task_data = client.post(TASKS_PATH, json=task).json()

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

    res = client.put(f"{TASKS_PATH}/{task_data["id"]}", json={"task_name": task_name})

    assert res.status_code == status.HTTP_200_OK
    assert res.json()["task_name"] == task_name


def test_update_invalid_task(client: TestClient, task):
    res = client.put(f"{TASKS_PATH}/0", json={"task_name": "task1"})

    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_update_task_without_value(client: TestClient):
    res = client.put(f"{TASKS_PATH}/1")

    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def delete_task(client: TestClient, task):
    task_data = client.post(TASKS_PATH, json=task).json()

    res = client.delete(f"{TASKS_PATH}/{task_data["id"]}")

    assert res.status_code == status.HTTP_204_NO_CONTENT


def delete_invalid_task(client: TestClient):
    res = client.delete(f"{TASKS_PATH}/0")

    assert res.status_code == status.HTTP_404_NOT_FOUND
