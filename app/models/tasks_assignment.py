from pydantic import BaseModel


class TasksAssignment(BaseModel):
    task_ids : list[int]
    technician_id : int