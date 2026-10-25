from fastapi import APIRouter, Depends, HTTPException
from datetime import date
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/")
async def read_tasks(db: Session = Depends(get_db)):
    tasks = crud.tasks.get_tasks(db)
    return tasks

@router.get("/{id}")
async def get_task_by_id(id: int, db: Session = Depends(get_db)):
    task = crud.tasks.get_task(db, id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"There is no task with id = {id}")
    return task


@router.post("/", status_code=201)
async def create_task(task: schemas.TaskCreator,  db: Session = Depends(get_db)):
    new_task = crud.tasks.create_task(task, db)
    if new_task is None:
        raise HTTPException(status_code=400, detail=f"Task creation was unsuccessful")
    return new_task

@router.put("/{id}")
async def put_task(id: int, task_data: schemas.TaskCreator, db: Session = Depends(get_db)):
    task = crud.tasks.update_task(id, task_data.model_dump(), db)
    if task is None:
        raise HTTPException(status_code=404, detail=f"There is not task with id = {id}")
    return task


@router.patch("/{id}")
async def patch_task(id: int, task_data: schemas.TaskUpdater, db: Session = Depends(get_db)):
    task = crud.tasks.update_task(id, task_data.model_dump(exclude_unset=True), db)
    if task is None:
        raise HTTPException(status_code=404, detail=f"There is not task with id = {id}")
    return task
    
@router.delete("/{id}", status_code=204)
async def delete_task(id: int, db: Session = Depends(get_db)):
    deletionIsSuccessful = crud.tasks.delete_task(id, db)
    if deletionIsSuccessful is None:
        raise HTTPException(status_code=404, detail=f"There is not task with id = {id}")
    
