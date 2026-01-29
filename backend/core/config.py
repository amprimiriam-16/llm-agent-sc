"""
Configuration Management
Loads settings from environment variables
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Azure OpenAI
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_DEPLOYMENT_NAME: str = "gpt-4"
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT: str = "text-embedding-ada-002"
    AZURE_OPENAI_API_VERSION: str = "2024-02-15-preview"
    
    # Azure Cosmos DB
    COSMOS_DB_ENDPOINT: str
    COSMOS_DB_KEY: str
    COSMOS_DB_DATABASE_NAME: str = "knowledge_base"
    COSMOS_DB_CONTAINER_NAME: str = "documents"
    COSMOS_DB_VECTOR_EMBEDDING_POLICY: bool = True
    
    # API Configuration
    API_ENDPOINT: str = "https://api.example.com/api"
    API_KEY: str = ""
    APPLY_ENABLED: bool = True
    
    # Application Settings
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    MAX_TOKENS: int = 4096
    TEMPERATURE: float = 0.7
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # MCP Configuration
    MCP_SERVER_PORT: int = 8001
    MCP_ENABLED: bool = True
    
    # FastAPI Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True
    
    # Streamlit Configuration
    STREAMLIT_PORT: int = 8501
    STREAMLIT_SERVER_ADDRESS: str = "localhost"
    
    # Security
    SECRET_KEY: str = "change-this-in-production"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:8501", "http://localhost:3000"]
    
    # Governance
    DATA_CLASSIFICATION: str = "CONFIDENTIAL"
    COMPLIANCE_MODE: str = "STANDARD"
    AUDIT_LOGGING: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
