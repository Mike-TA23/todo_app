from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import URL, create_engine, select
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
from datetime import date
from os import environ
from dotenv import load_dotenv

load_dotenv()
db_url = environ['DATABASE_URL']


class Base(DeclarativeBase): 
    pass

class TaskModel(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    status: Mapped[str]
    text: Mapped[str]
    deadline: Mapped[date]

engine = create_engine(db_url)
with Session(engine) as session:
    selectStmt = select(TaskModel)
    for i in session.scalars(selectStmt).all():
        print(i.title)

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

tasks = {0:    Task(
        id=0,
        name="doit",
        deadline="23-03-2043",
        importance=1,
        status=False
    )}

next_id = 1
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/tasks")
async def get_tasks():
    return tasks

@app.get("/tasks/{id}")
async def get_task_by_id(id: int):
    try:
        return tasks[id]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"There is no task with id = {id}")


@app.post("/tasks", status_code=201)
async def create_task(task: TaskCreator):
    global next_id
    new_task = Task(id = next_id, **task.model_dump())
    tasks[next_id] = new_task
    next_id += 1
    return  new_task

@app.put("/tasks/{id}")
async def put_task(id: int, task_data: TaskCreator):
    if id not in tasks:
        raise HTTPException(status_code=404, detail=f"There is no task with id = {id}")
    else:
        task = Task(id = id, **task_data.model_dump())
        tasks[id] = task
        return task


@app.patch("/tasks/{id}")
async def patch_task(id: int, task_data: TaskUpdater):
    try:
        task_updated_fields = {**task_data.model_dump(exclude_unset=True)}
        task = tasks[id]
        for key, value in task_updated_fields.items():
            setattr(task, key, value)
        return task
    except KeyError:       
        raise HTTPException(status_code=404, detail=f"There is not task with id = {id}")
    
@app.delete("/tasks/{id}", status_code=204)
async def delete_task(id: int):
    try:
        del tasks[id]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"There is not task with id = {id}")



