from sqlalchemy.orm import Session

from app.enums import TaskStatus
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def create(db: Session, data: TaskCreate) -> Task:
    task = Task(title=data.title, description=data.description)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_all(db: Session, status: TaskStatus | None = None) -> list[Task]:
    query = db.query(Task)
    if status is not None:
        query = query.filter(Task.status == status)
    return query.all()


def get_by_id(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id).first()


def update(db: Session, task: Task, data: TaskUpdate) -> Task:
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def complete(db: Session, task: Task) -> Task:
    task.status = TaskStatus.COMPLETED
    db.commit()
    db.refresh(task)
    return task


def delete(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
