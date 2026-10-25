from datetime import date
from pydantic import BaseModel

class TaskCreator(BaseModel):
    title: str
    text: str | None = None
    deadline: date   
    status: str

class TaskUpdater(BaseModel):
    title: str | None = None
    text: str | None = None
    deadline: date | None = None
    status: str | None = None

class Task(TaskCreator):
    id: int