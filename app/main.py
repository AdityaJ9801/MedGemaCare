"""Main FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import __version__
from app.api.routes import router
from app.api.patients import patients_router
from app.config import settings
from app.database import init_db
from app.models.model_loader import model_loader
from app.schemas.responses import ErrorResponse
from app.utils.logger import app_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    app_logger.info("Starting Medical Report Analysis API")
    init_db()
    app_logger.info("Patient database initialised")
    app_logger.info(f"Version: {__version__}")
    app_logger.info(f"Model: {settings.model_name}")

    # Check if ML dependencies are available (model loads lazily on first AI request)
    if not model_loader.is_available():
        app_logger.warning("ML dependencies not available. API will run in limited mode.")
        app_logger.warning("To enable ML features, install: pip install torch transformers accelerate")
    else:
        app_logger.info("ML dependencies available. Model will load on first AI request (lazy loading).")

    yield

    # Shutdown
    app_logger.info("Shutting down Medical Report Analysis API")
    if model_loader.is_loaded():
        model_loader.unload_model()


# Create FastAPI application
app = FastAPI(
    title="Medical Report Analysis API",
    description="Production-grade API for medical report summarization and analysis using MedGemma and RAG",
    version=__version__,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    app_logger.error(f"ValueError: {exc}")
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error="ValidationError",
            message=str(exc),
        ).model_dump(),
    )


@app.exception_handler(RuntimeError)
async def runtime_error_handler(request: Request, exc: RuntimeError):
    """Handle RuntimeError exceptions."""
    app_logger.error(f"RuntimeError: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="RuntimeError",
            message=str(exc),
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    app_logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="InternalServerError",
            message="An unexpected error occurred",
            detail=str(exc),
        ).model_dump(),
    )


# Include routers
app.include_router(router, prefix="/api/v1", tags=["Medical Reports"])
app.include_router(patients_router, tags=["Patient Management"])


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Medical Report Analysis API",
        "version": __version__,
        "status": "running",
        "docs": "/docs",
    }

