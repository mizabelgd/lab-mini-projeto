from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.enums import TaskStatus
from app.models.task import Task
from app.repository import task_repository
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(db: Session, data: TaskCreate, user_id: int) -> Task:
    return task_repository.create(db, data, user_id)


def list_tasks(db: Session, user_id: int, status: TaskStatus | None = None) -> list[Task]:
    return task_repository.get_all(db, user_id, status)


def get_task(db: Session, task_id: int, user_id: int) -> Task:
    task = task_repository.get_by_id(db, task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def update_task(db: Session, task_id: int, data: TaskUpdate, user_id: int) -> Task:
    task = get_task(db, task_id, user_id)
    return task_repository.update(db, task, data)


def complete_task(db: Session, task_id: int, user_id: int) -> Task:
    task = get_task(db, task_id, user_id)
    if task.status == TaskStatus.COMPLETED:
        raise HTTPException(status_code=409, detail="Task is already completed")
    return task_repository.complete(db, task)


def delete_task(db: Session, task_id: int, user_id: int) -> None:
    task = get_task(db, task_id, user_id)
    task_repository.delete(db, task)
