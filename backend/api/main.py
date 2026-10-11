from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.config import get_allowed_origins
from backend.api.routes.tasks import router as tasks_router

import logging

from fastapi import Request
from fastapi.responses import JSONResponse


app = FastAPI(
    title="EngineerFlow API",
    description="Multi-Agent AI Engineering Copilot",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


app.include_router(tasks_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "EngineerFlow API",
    }


logger = logging.getLogger(__name__)


@app.exception_handler(Exception)
async def handle_unexpected_error(
    request: Request,
    exc: Exception,
):
    logger.exception(
        "Unhandled API error on %s %s",
        request.method,
        request.url.path,
        exc_info=exc,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error."
        },
    )
