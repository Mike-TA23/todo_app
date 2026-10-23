from pydantic import BaseModel

class TaskCreator(BaseModel):
    name: str
    description: str | None = None
    deadline: str
    importance: int
    status: bool

class TaskUpdater(BaseModel):
    name: str | None = None
    description: str | None = None
    deadline: str | None = None
    importance: int | None = None
    status: bool | None = None

class Task(TaskCreator):
    id: int