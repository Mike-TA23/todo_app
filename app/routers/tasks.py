from fastapi import APIRouter, Depends, Query, HTTPException
from datetime import date
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=list[schemas.Task])
def read_tasks(
    db: Session = Depends(get_db),
    status: schemas.TaskStatus | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0, le=100)):
        tasks = crud.tasks.get_tasks(db, status=status, limit=limit, offset=offset)
        return tasks

@router.get("/{id}", response_model=schemas.Task)
def get_task_by_id(id: int, db: Session = Depends(get_db)):
    task = crud.tasks.get_task(db, id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"There is no task with id = {id}")
    return task


@router.post("/", status_code=201, response_model=schemas.Task)
def create_task(task: schemas.TaskCreator,  db: Session = Depends(get_db)):
    new_task = crud.tasks.create_task(task, db)
    if new_task is None:
        raise HTTPException(status_code=400, detail=f"Task creation was unsuccessful")
    return new_task

@router.put("/{id}", status_code=200, response_model=schemas.Task)
def put_task(id: int, task_data: schemas.TaskCreator, db: Session = Depends(get_db)):
    task = crud.tasks.update_task(id, task_data.model_dump(), db)
    if task is None:
        raise HTTPException(status_code=404, detail=f"There is not task with id = {id}")
    return task


@router.patch("/{id}", status_code=200, response_model=schemas.Task)
def patch_task(id: int, task_data: schemas.TaskUpdater, db: Session = Depends(get_db)):
    task = crud.tasks.update_task(id, task_data.model_dump(exclude_unset=True), db)
    if task is None:
        raise HTTPException(status_code=404, detail=f"There is not task with id = {id}")
    return task
    
@router.delete("/{id}", status_code=204)
def delete_task(id: int, db: Session = Depends(get_db)):
    deletionIsSuccessful = crud.tasks.delete_task(id, db)
    if deletionIsSuccessful is None:
        raise HTTPException(status_code=404, detail=f"There is not task with id = {id}")
    
