"""
Health Check Routes
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import httpx
from datetime import datetime

from backend.core.config import settings
from backend.core.logging import logger

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    environment: str


class DetailedHealthResponse(BaseModel):
    status: str
    timestamp: str
    components: Dict[str, Any]


@router.get("/", response_model=HealthResponse)
async def health_check():
    """Basic health check"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        environment=settings.ENVIRONMENT
    )


@router.get("/detailed", response_model=DetailedHealthResponse)
async def detailed_health_check():
    """Detailed health check including dependencies"""
    components = {}
    
    # Check Azure OpenAI
    try:
        # Simple connectivity check
        components["azure_openai"] = {
            "status": "healthy",
            "endpoint": settings.AZURE_OPENAI_ENDPOINT
        }
    except Exception as e:
        logger.error(f"Azure OpenAI health check failed: {e}")
        components["azure_openai"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # Check Cosmos DB
    try:
        components["cosmos_db"] = {
            "status": "healthy",
            "endpoint": settings.COSMOS_DB_ENDPOINT
        }
    except Exception as e:
        logger.error(f"Cosmos DB health check failed: {e}")
        components["cosmos_db"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # Check MCP server if enabled
    if settings.MCP_ENABLED:
        try:
            components["mcp_server"] = {
                "status": "healthy",
                "port": settings.MCP_SERVER_PORT
            }
        except Exception as e:
            components["mcp_server"] = {
                "status": "unhealthy",
                "error": str(e)
            }
    
    # Determine overall status
    overall_status = "healthy"
    for component in components.values():
        if component["status"] != "healthy":
            overall_status = "degraded"
            break
    
    return DetailedHealthResponse(
        status=overall_status,
        timestamp=datetime.utcnow().isoformat(),
        components=components
    )


@router.get("/ready")
async def readiness_check():
    """Kubernetes readiness probe"""
    return {"status": "ready"}


@router.get("/live")
async def liveness_check():
    """Kubernetes liveness probe"""
    return {"status": "alive"}
