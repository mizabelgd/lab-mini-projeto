from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="task-api")


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", timestamp=datetime.now(timezone.utc))