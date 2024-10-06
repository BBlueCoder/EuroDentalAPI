from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import Select
from sqlmodel import Session, and_, asc, desc, select
from starlette.requests import Request

from app.db.dependencies import get_session
from app.models.clients import Client
from app.models.products import Product
from app.models.task_products import TaskProduct
from app.models.tasks import Task, TaskCreate, TaskFilterParams, TaskRead, TaskUpdate
from app.models.users import User
from app.utils.global_utils import generate_the_address

router = APIRouter(prefix="/tasks", tags=["tasks"])


async def get_tasks(
    *,
    task_id: int | None = None,
    session: Session,
    req: Request,
    filter_params: TaskFilterParams = TaskFilterParams(),
) -> list[TaskRead]:
    statement: Select[tuple[Task, Client, User, TaskProduct, Product]] = (
        select(Task, Client, User, TaskProduct, Product)
        .join(Client, isouter=True)
        .join(User, User.id == Task.technician_id, isouter=True)
        .join(TaskProduct, isouter=True)
        .join(Product, TaskProduct.product_reference == Product.reference, isouter=True)
    )

    if task_id:
        statement = statement.where(Task.id == task_id)
    else:
        if filter_params.exact_date:
            statement = statement.where(Task.task_date == filter_params.exact_date)
        elif filter_params.date_range_start and filter_params.date_range_end:
            statement = statement.where(
                and_(
                    Task.task_date >= filter_params.date_range_start,
                    Task.task_date <= filter_params.date_range_end,
                )
            )

        order_by = (
            Task.task_date
            if filter_params.order_by == "task_date"
            else (
                Task.task_name
                if filter_params.order_by == "task_name"
                else Task.task_type
            )
        )
        sort_by = desc(order_by) if filter_params.sort == "desc" else asc(order_by)

        statement = statement.order_by(sort_by)

    tasks_with_details = session.exec(statement)

    mapped_results: list[TaskRead] = []

    for task, client, user, task_product, product in tasks_with_details:
        task_read = TaskRead(**task.model_dump())
        if client:
            task_read.client = f"{client.last_name} {client.first_name}"
            if client.image_id:
                task_read.client_image = generate_the_address(
                    req, f"images/{client.image_id}"
                )

        if user:
            task_read.technician = f"{user.last_name} {user.first_name}"
            if user.image_id:
                task_read.technician_image = generate_the_address(
                    req, f"images/{user.image_id}"
                )

        if product:
            if product.id_category:
                task_read.id_category = product.id_category
            if product.id_sub_category:
                task_read.id_sub_category = product.id_sub_category
            if product.id_brand:
                task_read.id_brand = product.id_brand

        mapped_results.append(task_read)

    return mapped_results


@router.get("/", response_model=list[TaskRead])
async def get_all_tasks(
    *,
    session: Session = Depends(get_session),
    req: Request,
    filter_params: TaskFilterParams = Depends(),
):
    return await get_tasks(session=session, req=req, filter_params=filter_params)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task_by_id(
    *, session: Session = Depends(get_session), task_id: int, req: Request
):
    task = await get_tasks(task_id=task_id, session=session, req=req)
    if not task:
        raise HTTPException(status_code=404, detail="Task Not Found")
    return task[0]


@router.post("/", response_model=TaskRead)
async def create_task(
    *, session: Session = Depends(get_session), task: TaskCreate, req: Request
):
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return (await get_tasks(task_id=db_task.id, session=session, req=req))[0]


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    *,
    session: Session = Depends(get_session),
    task: TaskUpdate,
    task_id: int,
    req: Request,
):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task Not Found")
    task_data = task.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(task_data)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return (await get_tasks(task_id=db_task.id, session=session, req=req))[0]


@router.delete("/{task_id}")
async def delete_task(*, session: Session = Depends(get_session), task_id: int):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task Not Found")
    session.delete(task)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
