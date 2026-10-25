from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


def get_task(db: Session, task_id: int):
    return db.get(models.TaskModel, task_id)


def get_tasks(db: Session):
    return db.scalars(select(models.TaskModel)).all()

def create_task(task: schemas.TaskCreator, db: Session):
    new_task = models.TaskModel(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def delete_task(task_id: int, db: Session):
    task = db.get(models.TaskModel, task_id)
    if task is None:
        return None
    db.delete(task)
    db.commit()
    return True

def update_task(task_id: int, changes: dict, db: Session):
    task = db.get(models.TaskModel, task_id)
    if task is None:
        return None
    for field, value in changes.items():
        setattr(task, field, value)
    db.commit()
    return task