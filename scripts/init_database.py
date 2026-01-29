"""
Database Initialization Script
Creates Cosmos DB database and container with vector indexing
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from backend.services.vector_store import CosmosDBVectorStore
from backend.core.logging import setup_logging, logger
from backend.core.config import settings


async def initialize_database():
    """Initialize Cosmos DB database and container"""
    try:
        setup_logging()
        logger.info("Starting database initialization...")
        
        # Create vector store (which initializes DB)
        vector_store = CosmosDBVectorStore()
        
        logger.info("✅ Database initialization complete!")
        logger.info(f"Database: {settings.COSMOS_DB_DATABASE_NAME}")
        logger.info(f"Container: {settings.COSMOS_DB_CONTAINER_NAME}")
        logger.info("Vector indexing enabled and configured")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("QA Platform - Database Initialization")
    print("=" * 60)
    
    success = asyncio.run(initialize_database())
    
    if success:
        print("\n✅ Initialization successful!")
        print("\nNext steps:")
        print("1. Run: python scripts/ingest_sample_data.py")
        print("2. Start backend: python -m uvicorn backend.main:app --reload")
        print("3. Start frontend: streamlit run frontend/app.py")
    else:
        print("\n❌ Initialization failed. Check logs for details.")
        sys.exit(1)
