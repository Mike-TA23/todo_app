from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])

next_id = 1
tasks = {0:    schemas.Task(
        id=0,
        name="doit",
        deadline="23-03-2043",
        importance=1,
        status=False
    )}

@router.get("/")
async def get_tasks():
    return tasks

@router.get("/{id}")
async def get_task_by_id(id: int):
    try:
        return tasks[id]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"There is no task with id = {id}")


@router.post("/", status_code=201)
async def create_task(task: schemas.TaskCreator):
    global next_id
    new_task = schemas.Task(id = next_id, **task.model_dump())
    tasks[next_id] = new_task
    next_id += 1
    return  new_task

@router.put("/{id}")
async def put_task(id: int, task_data: schemas.TaskCreator):
    if id not in tasks:
        raise HTTPException(status_code=404, detail=f"There is no task with id = {id}")
    else:
        task = schemas.Task(id = id, **task_data.model_dump())
        tasks[id] = task
        return task


@router.patch("/{id}")
async def patch_task(id: int, task_data: schemas.TaskUpdater):
    try:
        task_updated_fields = {**task_data.model_dump(exclude_unset=True)}
        task = tasks[id]
        for key, value in task_updated_fields.items():
            setattr(task, key, value)
        return task
    except KeyError:       
        raise HTTPException(status_code=404, detail=f"There is not task with id = {id}")
    
@router.delete("/{id}", status_code=204)
async def delete_task(id: int):
    try:
        del tasks[id]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"There is not task with id = {id}")
