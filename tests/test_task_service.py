from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.enums import TaskStatus
from app.service import task_service


def _mock_task(status: TaskStatus = TaskStatus.PENDING) -> MagicMock:
    t = MagicMock()
    t.status = status
    return t


def test_get_task_raises_404_when_not_found() -> None:
    db = MagicMock()
    with patch("app.service.task_service.task_repository.get_by_id", return_value=None):
        with pytest.raises(HTTPException) as exc:
            task_service.get_task(db, task_id=1, user_id=1)
    assert exc.value.status_code == 404


def test_complete_task_raises_409_when_already_completed() -> None:
    db = MagicMock()
    with patch(
        "app.service.task_service.task_repository.get_by_id",
        return_value=_mock_task(TaskStatus.COMPLETED),
    ):
        with pytest.raises(HTTPException) as exc:
            task_service.complete_task(db, task_id=1, user_id=1)
    assert exc.value.status_code == 409


def test_delete_task_raises_404_when_not_found() -> None:
    db = MagicMock()
    with patch("app.service.task_service.task_repository.get_by_id", return_value=None):
        with pytest.raises(HTTPException) as exc:
            task_service.delete_task(db, task_id=1, user_id=1)
    assert exc.value.status_code == 404


def test_create_task_passes_user_id_to_repository() -> None:
    db = MagicMock()
    data = MagicMock()
    expected = _mock_task()
    with patch(
        "app.service.task_service.task_repository.create", return_value=expected
    ) as mock_create:
        result = task_service.create_task(db, data, user_id=42)
    mock_create.assert_called_once_with(db, data, 42)
    assert result is expected


def test_list_tasks_passes_status_filter_to_repository() -> None:
    db = MagicMock()
    with patch(
        "app.service.task_service.task_repository.get_all", return_value=[]
    ) as mock_get_all:
        task_service.list_tasks(db, user_id=1, status=TaskStatus.PENDING)
    mock_get_all.assert_called_once_with(db, 1, TaskStatus.PENDING)
