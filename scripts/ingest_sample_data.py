"""
Sample Data Ingestion Script
Loads sample documents into the vector store
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


async def ingest_sample_data():
    """Ingest sample documents"""
    try:
        setup_logging()
        logger.info("Starting sample data ingestion...")
        
        # Initialize vector store
        vector_store = CosmosDBVectorStore()
        
        # Get sample documents directory
        data_dir = Path(__file__).parent.parent / "data" / "sample" / "supply_chain_docs"
        
        if not data_dir.exists():
            logger.error(f"Sample data directory not found: {data_dir}")
            return False
        
        # Get all text files
        sample_files = list(data_dir.glob("*.txt"))
        
        if not sample_files:
            logger.warning(f"No sample files found in {data_dir}")
            return False
        
        logger.info(f"Found {len(sample_files)} sample documents")
        
        # Ingest each document
        for file_path in sample_files:
            logger.info(f"Processing: {file_path.name}")
            
            try:
                doc_id = await vector_store.add_document(
                    file_path=str(file_path),
                    filename=file_path.name,
                    metadata={
                        "classification": "CONFIDENTIAL",
                        "source": "Sample Data",
                        "category": "Supply Chain Documentation"
                    }
                )
                
                logger.info(f"✅ Ingested: {file_path.name} (ID: {doc_id})")
                
            except Exception as e:
                logger.error(f"❌ Failed to ingest {file_path.name}: {e}")
        
        logger.info("✅ Sample data ingestion complete!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Data ingestion failed: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("QA Platform - Sample Data Ingestion")
    print("=" * 60)
    
    success = asyncio.run(ingest_sample_data())
    
    if success:
        print("\n✅ Sample data ingestion successful!")
        print("\nThe knowledge base now contains supply chain documents.")
        print("\nYou can now:")
        print("1. Start the backend: python -m uvicorn backend.main:app --reload")
        print("2. Start the frontend: streamlit run frontend/app.py")
        print("3. Ask questions about supply chain, procurement, logistics, etc.")
    else:
        print("\n❌ Ingestion failed. Check logs for details.")
        sys.exit(1)
