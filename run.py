"""Entry point for running the Medical Report Analysis API."""

import uvicorn

from app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        workers=settings.api_workers,
        reload=settings.api_reload,
        log_level=settings.log_level.lower(),
    )

