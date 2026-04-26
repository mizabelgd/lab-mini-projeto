from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.enums import TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: str | None = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("title cannot be empty")
        return v.strip()


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("title cannot be empty")
        return v.strip() if v else v


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
