from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session, select
from app.db.dependencies import get_session
from app.models.tasks import TaskRead, Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskRead])
async def get_all_tasks(*, session: Session = Depends(get_session)):
    return session.exec(select(Task)).all()


@router.get("/{task_id}", response_model=TaskRead)
async def get_task_by_id(
    *, session: Session = Depends(get_session), task_id: int
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task Not Found")
    return task


@router.post("/", response_model=TaskRead)
async def create_task(
    *, session: Session = Depends(get_session), task: TaskCreate
):
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    *,
    session: Session = Depends(get_session),
    task: TaskUpdate,
    task_id: int
):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task Not Found")
    task_data = task.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(task_data)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.delete("/{task_id}")
async def delete_task(*, session: Session = Depends(get_session), task_id: int):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task Not Found")
    session.delete(task)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
