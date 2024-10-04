from email.policy import default

from sqlmodel import SQLModel, Field
from datetime import date


class TaskBase(SQLModel):
    task_name: str | None = Field(default=None, max_length=50, description="Name of the task, up to 50 characters.")
    task_type: str | None = Field(default=None, max_length=50, description="Type of the task, up to 50 characters.")
    description: str | None = Field(default=None, description="Detailed description of the task.")
    technician_id: int | None = Field(default=None, description="ID of the technician assigned to the task, optional.",
                                      foreign_key="users.id")
    task_date: date | None = Field(default=None, description="Date the task is scheduled or created.")
    observation: str | None = Field(default=None, description="Additional observations or notes related to the task.")


class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(None, primary_key=True)
    create_by: int = Field(description="ID of the user who created the task, required field.", foreign_key="users.id")
    client_id: int = Field(description="ID of the client associated with the task, required field.",
                           foreign_key="clients.id")
    status: str = Field(max_length=50, description="Current status of the task, required field.")


class TaskCreate(TaskBase):
    create_by: int = Field(description="ID of the user who created the task, required field.", foreign_key="users.id")
    client_id: int = Field(description="ID of the client associated with the task, required field.",
                           foreign_key="clients.id")
    status: str = Field(max_length=50, description="Current status of the task, required field.")


class TaskUpdate(TaskBase):
    create_by: int |None  = Field(default=None,description="ID of the user who created the task, required field.", foreign_key="users.id")
    client_id: int | None= Field(default=None,description="ID of the client associated with the task, required field.",
                           foreign_key="clients.id")
    status: str | None= Field(default=None,max_length=50, description="Current status of the task, required field.")


class TaskRead(TaskBase):
    id: int
    create_by: int = Field(description="ID of the user who created the task, required field.", foreign_key="users.id")
    client_id: int = Field(description="ID of the client associated with the task, required field.",
                           foreign_key="clients.id")
    status: str = Field(max_length=50, description="Current status of the task, required field.")