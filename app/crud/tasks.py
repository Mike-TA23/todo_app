from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


def get_task(db: Session, task_id: int):
    return db.get(models.Task, task_id)


def get_tasks(db: Session):
    return db.scalars(select(models.Task)).all()