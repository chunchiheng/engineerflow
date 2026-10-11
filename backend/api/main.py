
from fastapi import FastAPI

from backend.api.routes.tasks import router as tasks_router


app = FastAPI(
    title="EngineerFlow API",
    description="Multi-Agent AI Engineering Copilot",
    version="0.1.0",
)


app.include_router(tasks_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "EngineerFlow API",
    }
