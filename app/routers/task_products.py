from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session, select

from app.controllers.task_products_controller import TaskProductController
from app.db.dependencies import get_session
from app.models.task_products import (TaskProduct, TaskProductCreate,
                                      TaskProductRead, TaskProductUpdate, TaskProductUpdateQuantity)
from app.models.users import User
from app.routers.auth import authorize
from app.utils.global_utils import global_prefix

router = APIRouter(prefix=f"{global_prefix}/task_products", tags=["task_products"])


@router.get("/", response_model=list[TaskProductRead])
async def get_all_task_products(*, session: Session = Depends(get_session), user: User = Depends(authorize)):
    controller = TaskProductController(session)
    return await controller.get_task_products()


@router.get("/{task_products_id}", response_model=TaskProductRead)
async def get_task_products_by_id(
        *, session: Session = Depends(get_session), task_products_id: int
        , user: User = Depends(authorize)):
    controller = TaskProductController(session)
    return await controller.get_task_product_by_id(task_products_id)


@router.post("/", response_model=TaskProductRead)
async def create_task_products(
        *, session: Session = Depends(get_session), task_products: TaskProductCreate
        , user: User = Depends(authorize)):
    controller = TaskProductController(session)
    return await controller.create_task_product(task_products)


@router.put("/{task_products_id}")
async def update_task_products(
        *,
        session: Session = Depends(get_session),
        task_products: TaskProductUpdate,
        task_products_id: int
        , user: User = Depends(authorize)):
    controller = TaskProductController(session)
    await controller.update_task_product(task_products, task_products_id)
    return "prodact has been updated successfully"


@router.put("/quantity/{task_products_id}", response_model=TaskProductRead)
async def update_task_products(
        *,
        session: Session = Depends(get_session),
        task_products_id: int,
        task_product_update_quantity: TaskProductUpdateQuantity
        , user: User = Depends(authorize)):
    controller = TaskProductController(session)
    return await controller.update_product_quantity(task_products_id,
                                                    task_product_update_quantity.new_quantity)


@router.delete("/{task_products_id}")
async def delete_task_products(
        *, session: Session = Depends(get_session), task_products_id: int
        , user: User = Depends(authorize)):
    controller = TaskProductController(session)
    await controller.delete_task_product(task_products_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
