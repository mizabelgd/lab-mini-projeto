import pytest
from sqlalchemy.orm import Session

from app.enums import TaskStatus
from app.models.user import User
from app.repository import task_repository, user_repository
from app.schemas.task import TaskCreate, TaskUpdate


@pytest.fixture()
def user(db: Session) -> User:
    return user_repository.create(db, "repo@test.com", "hashed_pw")


def test_create_sets_pending_status(db: Session, user: User) -> None:
    task = task_repository.create(db, TaskCreate(title="Test"), user.id)
    assert task.id is not None
    assert task.status == TaskStatus.PENDING


def test_get_all_returns_only_owner_tasks(db: Session, user: User) -> None:
    other = user_repository.create(db, "other@test.com", "hashed_pw")
    task_repository.create(db, TaskCreate(title="Mine"), user.id)
    task_repository.create(db, TaskCreate(title="Theirs"), other.id)

    tasks = task_repository.get_all(db, user.id)
    assert len(tasks) == 1
    assert tasks[0].title == "Mine"


def test_get_all_filters_by_status(db: Session, user: User) -> None:
    t = task_repository.create(db, TaskCreate(title="A"), user.id)
    task_repository.create(db, TaskCreate(title="B"), user.id)
    task_repository.complete(db, t)

    assert len(task_repository.get_all(db, user.id, TaskStatus.PENDING)) == 1
    assert len(task_repository.get_all(db, user.id, TaskStatus.COMPLETED)) == 1
    assert len(task_repository.get_all(db, user.id)) == 2


def test_get_by_id_returns_none_for_wrong_user(db: Session, user: User) -> None:
    other = user_repository.create(db, "other@test.com", "hashed_pw")
    task = task_repository.create(db, TaskCreate(title="Test"), user.id)
    assert task_repository.get_by_id(db, task.id, other.id) is None


def test_update_task(db: Session, user: User) -> None:
    task = task_repository.create(db, TaskCreate(title="Old"), user.id)
    updated = task_repository.update(db, task, TaskUpdate(title="New", description="Desc"))
    assert updated.title == "New"
    assert updated.description == "Desc"


def test_complete_task(db: Session, user: User) -> None:
    task = task_repository.create(db, TaskCreate(title="Test"), user.id)
    completed = task_repository.complete(db, task)
    assert completed.status == TaskStatus.COMPLETED


def test_delete_task(db: Session, user: User) -> None:
    task = task_repository.create(db, TaskCreate(title="Test"), user.id)
    task_id = task.id
    task_repository.delete(db, task)
    assert task_repository.get_by_id(db, task_id, user.id) is None
