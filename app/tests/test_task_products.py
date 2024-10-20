from statistics import quantiles

import pytest
from fastapi import status
from markdown_it.rules_block import reference
from sqlmodel import Session
from starlette.testclient import TestClient

from app.models.clients import Client
from app.models.products import Product
from app.models.tasks import Task
from app.models.users import User
from app.utils.global_utils import global_prefix

TASK_PRODUCTS_PATH = f"{global_prefix}/task_products"
task_products = [
    "task_product1",
    "task_product2",
    "task_product3",
]


@pytest.fixture(name="task")
def task_fixture(session: Session, client_db: Client, user_db: User):
    task_dic = {
        "task_name": "task1",
        "client_id": client_db.id,
        "create_by": user_db.id,
        "status": "In Progress",
    }
    task = Task(**task_dic)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def test_get_all_task_products(client: TestClient):
    res = client.get(TASK_PRODUCTS_PATH)
    assert res.status_code == status.HTTP_200_OK


def test_create_task_products(client: TestClient, product: Product, task: Task):
    task_product = {
        "product_reference": product.reference,
        "task_id": task.id,
        "price": 35,
        "quantity": 5,
    }
    res = client.post(TASK_PRODUCTS_PATH, json=task_product)
    assert res.status_code == status.HTTP_200_OK
    res_data = res.json()
    assert res_data["product_reference"] == task_product["product_reference"]
    assert res_data["task_id"] == task_product["task_id"]
    assert res_data["price"] == task_product["price"]
    assert res_data["quantity"] == task_product["quantity"]
    assert res_data["id"] == 1
    assert res_data["purchase_date"] is not None


def test_create_task_product_without_value(client: TestClient):
    res = client.post(TASK_PRODUCTS_PATH)

    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_and_get_task_products(client: TestClient, product: Product, task: Task):
    for task_product in task_products:
        client.post(
            TASK_PRODUCTS_PATH,
            json={"product_reference": product.reference, "task_id": task.id},
        )

    res = client.get(TASK_PRODUCTS_PATH)
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == len(task_products)


def test_get_task_product_by_id(client: TestClient, product: Product, task: Task):
    task_product_data = client.post(
        TASK_PRODUCTS_PATH,
        json={"product_reference": product.reference, "task_id": task.id},
    ).json()

    res = client.get(f"{TASK_PRODUCTS_PATH}/{task_product_data["id"]}")
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["task_id"] == task.id


def test_get_invalid_task_product_by_id(client: TestClient):
    res = client.get(f"{TASK_PRODUCTS_PATH}/0")
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "price",
    [
        55,
        66,
        78,
    ],
)
def test_update_task_product(
    client: TestClient, price: float, product: Product, task: Task
):
    task_product_data = client.post(
        TASK_PRODUCTS_PATH,
        json={
            "quantity": 5,
            "product_reference": product.reference,
            "task_id": task.id,
        },
    ).json()

    res = client.put(
        f"{TASK_PRODUCTS_PATH}/{task_product_data["id"]}", json={"price": price}
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.json()["price"] == price
    assert res.json()["quantity"] == 5


def test_update_invalid_task_product(client: TestClient):
    res = client.put(f"{TASK_PRODUCTS_PATH}/0", json={"price": 30})

    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_update_task_product_without_value(client: TestClient):
    res = client.put(f"{TASK_PRODUCTS_PATH}/1")

    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def delete_task_product(client: TestClient, product: Product, task: Task):
    task_product_data = client.post(
        TASK_PRODUCTS_PATH,
        json={"product_reference": product.reference, "task_id": task.id},
    ).json()

    res = client.delete(f"{TASK_PRODUCTS_PATH}/{task_product_data["id"]}")

    assert res.status_code == status.HTTP_204_NO_CONTENT


def delete_invalid_task_product(client: TestClient):
    res = client.delete(f"{TASK_PRODUCTS_PATH}/0")

    assert res.status_code == status.HTTP_404_NOT_FOUND
