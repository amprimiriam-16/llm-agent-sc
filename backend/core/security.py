"""
Security and Authentication
"""
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from backend.core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)):
    """Verify API key for authentication"""
    if settings.ENVIRONMENT == "development":
        return True
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key"
        )
    
    # In production, validate against stored API keys
    # For now, simple validation
    if api_key != settings.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    
    return True
