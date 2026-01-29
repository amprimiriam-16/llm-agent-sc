"""
Test Azure Connections
Verify connectivity to Azure services
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from backend.core.config import settings
from backend.core.logging import setup_logging, logger
from backend.services.embeddings import EmbeddingService
from backend.services.llm import LLMService
from azure.cosmos import CosmosClient


async def test_azure_openai():
    """Test Azure OpenAI connection"""
    try:
        print("\n🧪 Testing Azure OpenAI...")
        
        # Test embeddings
        embedding_service = EmbeddingService()
        embedding = await embedding_service.embed_text("Test connection")
        print(f"✅ Embeddings working - dimension: {len(embedding)}")
        
        # Test LLM
        llm_service = LLMService()
        response = await llm_service.generate_response(
            prompt="Say 'Connection successful' if you can read this.",
            temperature=0.1,
            max_tokens=50
        )
        print(f"✅ LLM working - response: {response[:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ Azure OpenAI test failed: {e}")
        return False


def test_cosmos_db():
    """Test Cosmos DB connection"""
    try:
        print("\n🧪 Testing Azure Cosmos DB...")
        
        client = CosmosClient(
            settings.COSMOS_DB_ENDPOINT,
            credential=settings.COSMOS_DB_KEY
        )
        
        # List databases
        databases = list(client.list_databases())
        print(f"✅ Cosmos DB connected - found {len(databases)} databases")
        
        return True
    except Exception as e:
        print(f"❌ Cosmos DB test failed: {e}")
        return False


async def run_tests():
    """Run all connection tests"""
    setup_logging()
    
    print("=" * 60)
    print("QA Platform - Azure Connection Tests")
    print("=" * 60)
    
    print(f"\nConfiguration:")
    print(f"Azure OpenAI Endpoint: {settings.AZURE_OPENAI_ENDPOINT}")
    print(f"Cosmos DB Endpoint: {settings.COSMOS_DB_ENDPOINT}")
    print(f"Environment: {settings.ENVIRONMENT}")
    
    # Run tests
    results = []
    
    results.append(await test_azure_openai())
    results.append(test_cosmos_db())
    
    # Summary
    print("\n" + "=" * 60)
    if all(results):
        print("✅ All tests passed! Azure connections are working.")
        print("\nYou can now proceed with:")
        print("1. python scripts/init_database.py")
        print("2. python scripts/ingest_sample_data.py")
        return True
    else:
        print("❌ Some tests failed. Please check your configuration.")
        print("\nVerify your .env file contains correct:")
        print("- AZURE_OPENAI_ENDPOINT")
        print("- AZURE_OPENAI_API_KEY")
        print("- COSMOS_DB_ENDPOINT")
        print("- COSMOS_DB_KEY")
        return False


if __name__ == "__main__":
    success = asyncio.run(run_tests())
    sys.exit(0 if success else 1)
