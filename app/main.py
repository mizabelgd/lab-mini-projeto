from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel

from app.controller.task_controller import router as task_router
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="task-api")

app.include_router(task_router)


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", timestamp=datetime.now(timezone.utc))
