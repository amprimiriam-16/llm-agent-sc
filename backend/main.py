"""
FastAPI Backend Main Application
SCIP Question-Answering Platform
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time

from backend.core.config import settings
from backend.core.logging import setup_logging, logger
from backend.api.routes import chat, documents, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting SCIP QA Platform API")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Azure OpenAI Endpoint: {settings.AZURE_OPENAI_ENDPOINT}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down SCIP QA Platform API")


# Initialize FastAPI app
app = FastAPI(
    title="SCIP Question-Answering Platform API",
    description="Enterprise RAG platform for BASF Supply Chain Intelligence",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Setup logging
setup_logging()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Audit logging
    if settings.AUDIT_LOGGING:
        logger.info(
            "request_completed",
            method=request.method,
            url=str(request.url),
            process_time=process_time,
            status_code=response.status_code
        )
    
    return response


# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal error occurred",
            "type": type(exc).__name__
        }
    )


# Include routers
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "SCIP Question-Answering Platform",
        "version": "1.0.0",
        "status": "operational",
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD
    )
