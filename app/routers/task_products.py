from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session, select

from app.db.dependencies import get_session
from app.models.task_products import (TaskProduct, TaskProductCreate,
                                      TaskProductRead, TaskProductUpdate)
from app.models.users import User
from app.routers.auth import authorize
from app.utils.global_utils import global_prefix

router = APIRouter(prefix=f"{global_prefix}/task_products", tags=["task_products"])


@router.get("/", response_model=list[TaskProductRead])
async def get_all_task_products(*, session: Session = Depends(get_session),user : User = Depends(authorize)):
    return session.exec(select(TaskProduct)).all()


@router.get("/{task_products_id}", response_model=TaskProductRead)
async def get_task_products_by_id(
    *, session: Session = Depends(get_session), task_products_id: int
,user : User = Depends(authorize)):
    task_products = session.get(TaskProduct, task_products_id)
    if not task_products:
        raise HTTPException(status_code=404, detail="TaskProduct Not Found")
    return task_products


@router.post("/", response_model=TaskProductRead)
async def create_task_products(
    *, session: Session = Depends(get_session), task_products: TaskProductCreate
,user : User = Depends(authorize)):
    db_task_products = TaskProduct.model_validate(task_products)
    session.add(db_task_products)
    session.commit()
    session.refresh(db_task_products)
    return db_task_products


@router.put("/{task_products_id}", response_model=TaskProductRead)
async def update_task_products(
    *,
    session: Session = Depends(get_session),
    task_products: TaskProductUpdate,
    task_products_id: int
,user : User = Depends(authorize)):
    db_task_products = session.get(TaskProduct, task_products_id)
    if not db_task_products:
        raise HTTPException(status_code=404, detail="TaskProduct Not Found")
    task_products_data = task_products.model_dump(exclude_unset=True)
    db_task_products.sqlmodel_update(task_products_data)
    session.add(db_task_products)
    session.commit()
    session.refresh(db_task_products)
    return db_task_products


@router.delete("/{task_products_id}")
async def delete_task_products(
    *, session: Session = Depends(get_session), task_products_id: int
,user : User = Depends(authorize)):
    task_products = session.get(TaskProduct, task_products_id)
    if not task_products:
        raise HTTPException(status_code=404, detail="TaskProduct Not Found")
    session.delete(task_products)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
