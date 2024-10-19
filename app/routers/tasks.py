from fastapi import APIRouter, Depends, Response, status
from sqlmodel import Session
from starlette.requests import Request

from app.controllers.tasks_controller import TasksController
from app.db.dependencies import get_session
from app.models.tasks import (Task, TaskCreate, TaskFilterParams, TaskRead,
                              TaskUpdate)
from app.models.users import User
from app.routers.auth import authorize
from app.utils.global_utils import global_prefix

router = APIRouter(prefix=f"{global_prefix}/tasks", tags=["tasks"])

@router.get("/", response_model=list[TaskRead])
async def get_all_tasks(
        *,
        session: Session = Depends(get_session),
        req: Request,
        filter_params: TaskFilterParams = Depends()
        , user: User = Depends(authorize)):
    controller = TasksController(session,req)
    return await controller.get_tasks(filter_params)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task_by_id(
        *, session: Session = Depends(get_session), task_id: int, req: Request
        , user: User = Depends(authorize)):
    controller = TasksController(session, req)
    return await controller.get_task_by_id(task_id)


@router.post("/", response_model=TaskRead)
async def create_task(
        *, session: Session = Depends(get_session), task: TaskCreate, req: Request
        , user: User = Depends(authorize)):
    controller = TasksController(session, req)
    return await controller.create_task(task)


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
        *,
        session: Session = Depends(get_session),
        task: TaskUpdate,
        task_id: int,
        req: Request
        , user: User = Depends(authorize)):
    controller = TasksController(session, req)
    return await controller.update_task(task,task_id)


@router.delete("/{task_id}")
async def delete_task(*, session: Session = Depends(get_session), task_id: int, user: User = Depends(authorize)):
    controller = TasksController(session)
    await controller.delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
