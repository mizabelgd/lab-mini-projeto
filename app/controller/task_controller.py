from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import CurrentUser
from app.enums import TaskStatus
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.service import task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(),
) -> TaskResponse:
    return task_service.create_task(db, data, current_user.id)


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    status: TaskStatus | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(),
) -> list[TaskResponse]:
    return task_service.list_tasks(db, current_user.id, status)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(),
) -> TaskResponse:
    return task_service.get_task(db, task_id, current_user.id)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(),
) -> TaskResponse:
    return task_service.update_task(db, task_id, data, current_user.id)


@router.patch("/{task_id}/complete", response_model=TaskResponse)
def complete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(),
) -> TaskResponse:
    return task_service.complete_task(db, task_id, current_user.id)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(),
) -> None:
    task_service.delete_task(db, task_id, current_user.id)
