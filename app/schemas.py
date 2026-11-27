from datetime import date
from pydantic import BaseModel, field_validator
from typing import Literal

TaskStatus = Literal["pending", "in_progress", "completed"]

class TaskCreator(BaseModel):
    title: str
    text: str | None = None
    deadline: date   
    status: TaskStatus

class TaskUpdater(BaseModel):
    title: str | None = None
    text: str | None = None
    deadline: date | None = None
    status: TaskStatus | None = None

    @field_validator("status")
    @classmethod
    def reject_null_status(cls, value):
        if value is None:
            raise ValueError("status cannot be null")
        return value

class Task(TaskCreator):
    id: int