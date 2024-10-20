from datetime import date
from email.policy import default
from enum import Enum
from typing import Literal

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

class Status(str, Enum):
    unassigned = "Unassigned"
    in_progress = "In Progress"
    completed = "Completed"

class TaskBase(SQLModel):
    task_name: str | None = Field(
        default=None,
        max_length=50,
        description="Name of the task, up to 50 characters.",
    )
    task_type: str | None = Field(
        default=None,
        max_length=50,
        description="Type of the task, up to 50 characters.",
    )
    description: str | None = Field(
        default=None, description="Detailed description of the task."
    )
    technician_id: int | None = Field(
        default=None,
        description="ID of the technician assigned to the task, optional.",
        foreign_key="users.id",
    )
    task_date: date | None = Field(
        default=None, description="Date the task is scheduled or created."
    )
    observation: str | None = Field(
        default=None,
        description="Additional observations or notes related to the task.",
    )


class TaskWithIDs(TaskBase):
    create_by: int | None = Field(
        None,
        description="ID of the user who created the task, required field.",
        foreign_key="users.id",
    )
    client_id: int = Field(
        description="ID of the client associated with the task, required field.",
        foreign_key="clients.id",
    )
    status: Status |None = Field(
        Status.unassigned,max_length=50, description="Current status of the task, required field."
    )


class Task(TaskWithIDs, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(None, primary_key=True)


class TaskCreate(TaskWithIDs):
    pass


class TaskUpdate(TaskBase):
    create_by: int | None = Field(
        default=None,
        description="ID of the user who created the task, required field.",
        foreign_key="users.id",
    )
    client_id: int | None = Field(
        default=None,
        description="ID of the client associated with the task, required field.",
        foreign_key="clients.id",
    )
    status: Status | None = Field(
        default=None,
        max_length=50,
        description="Current status of the task, required field.",
    )


class TaskRead(TaskWithIDs):
    id: int
    client: str | None = None
    client_image: str | None = None
    technician: str | None = None
    technician_image: str | None = None
    # id_category: int | None = None
    # id_sub_category: int | None = None
    # id_brand: int | None = None


class TaskFilterParams(BaseModel):
    order_by: Literal["task_date", "task_name", "task_type"] = "task_date"
    sort: Literal["asc", "desc"] = "desc"
    exact_date: date | None = None
    date_range_start: date | None = None
    date_range_end: date | None = None
