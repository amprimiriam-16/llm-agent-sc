"""
Azure Cosmos DB Vector Store
Handles vector embeddings storage and retrieval
"""
from typing import List, Dict, Any, Optional
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosHttpResponseError
import uuid
from datetime import datetime

from backend.core.config import settings
from backend.core.logging import logger
from backend.services.embeddings import EmbeddingService


class CosmosDBVectorStore:
    """Azure Cosmos DB Vector Store with vector search capabilities"""
    
    def __init__(self):
        self.client = CosmosClient(
            settings.COSMOS_DB_ENDPOINT,
            credential=settings.COSMOS_DB_KEY
        )
        self.database_name = settings.COSMOS_DB_DATABASE_NAME
        self.container_name = settings.COSMOS_DB_CONTAINER_NAME
        self.embedding_service = EmbeddingService()
        
        # Initialize database and container
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize Cosmos DB database and container with vector indexing"""
        try:
            # Create database if not exists
            self.database = self.client.create_database_if_not_exists(
                id=self.database_name
            )
            logger.info(f"Database '{self.database_name}' ready")
            
            # Vector indexing policy
            indexing_policy = {
                "indexingMode": "consistent",
                "automatic": True,
                "includedPaths": [{"path": "/*"}],
                "excludedPaths": [{"path": "/\"_etag\"/?"}],
                "vectorIndexes": [
                    {
                        "path": "/embedding",
                        "type": "quantizedFlat"
                    }
                ]
            }
            
            # Vector embedding policy for Cosmos DB
            vector_embedding_policy = {
                "vectorEmbeddings": [
                    {
                        "path": "/embedding",
                        "dataType": "float32",
                        "distanceFunction": "cosine",
                        "dimensions": 1536  # Azure OpenAI ada-002 dimension
                    }
                ]
            }
            
            # Create container with vector support
            self.container = self.database.create_container_if_not_exists(
                id=self.container_name,
                partition_key=PartitionKey(path="/document_id"),
                indexing_policy=indexing_policy,
                vector_embedding_policy=vector_embedding_policy if settings.COSMOS_DB_VECTOR_EMBEDDING_POLICY else None
            )
            logger.info(f"Container '{self.container_name}' ready with vector indexing")
            
        except CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB initialization error: {e}")
            raise
    
    async def add_document(
        self,
        file_path: str,
        filename: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Add document to vector store
        
        Args:
            file_path: Path to document file
            filename: Original filename
            metadata: Additional metadata
            
        Returns:
            Document ID
        """
        try:
            # Read and chunk document
            chunks = await self._chunk_document(file_path)
            document_id = str(uuid.uuid4())
            
            # Process each chunk
            for i, chunk in enumerate(chunks):
                # Generate embedding
                embedding = await self.embedding_service.embed_text(chunk["text"])
                
                # Prepare document for Cosmos DB
                item = {
                    "id": f"{document_id}_chunk_{i}",
                    "document_id": document_id,
                    "filename": filename,
                    "chunk_index": i,
                    "content": chunk["text"],
                    "embedding": embedding,
                    "metadata": {
                        **(metadata or {}),
                        "total_chunks": len(chunks),
                        "char_count": len(chunk["text"]),
                        "created_at": datetime.utcnow().isoformat()
                    }
                }
                
                # Insert into Cosmos DB
                self.container.create_item(body=item)
            
            logger.info(f"Document '{filename}' indexed with {len(chunks)} chunks")
            return document_id
            
        except Exception as e:
            logger.error(f"Error adding document: {e}", exc_info=True)
            raise
    
    async def _chunk_document(self, file_path: str) -> List[Dict[str, Any]]:
        """Chunk document into smaller pieces"""
        # Simple text chunking - enhance with LangChain text splitters
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            
            # Simple chunking by character count
            chunk_size = settings.CHUNK_SIZE
            chunk_overlap = settings.CHUNK_OVERLAP
            chunks = []
            
            for i in range(0, len(text), chunk_size - chunk_overlap):
                chunk_text = text[i:i + chunk_size]
                if chunk_text.strip():
                    chunks.append({
                        "text": chunk_text,
                        "start_index": i
                    })
            
            return chunks if chunks else [{"text": text, "start_index": 0}]
            
        except Exception as e:
            logger.error(f"Error chunking document: {e}")
            raise
    
    async def similarity_search(
        self,
        query: str,
        max_results: int = 5,
        min_score: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Perform vector similarity search
        
        Args:
            query: Search query
            max_results: Maximum number of results
            min_score: Minimum similarity score
            
        Returns:
            List of relevant documents with scores
        """
        try:
            # Generate query embedding
            query_embedding = await self.embedding_service.embed_text(query)
            
            # Cosmos DB vector search query
            # Note: Actual vector search syntax may vary based on Cosmos DB version
            query_spec = {
                "query": """
                    SELECT TOP @max_results 
                        c.id, 
                        c.document_id, 
                        c.filename, 
                        c.content, 
                        c.metadata,
                        VectorDistance(c.embedding, @query_embedding) AS score
                    FROM c
                    WHERE VectorDistance(c.embedding, @query_embedding) > @min_score
                    ORDER BY VectorDistance(c.embedding, @query_embedding) DESC
                """,
                "parameters": [
                    {"name": "@max_results", "value": max_results},
                    {"name": "@query_embedding", "value": query_embedding},
                    {"name": "@min_score", "value": min_score}
                ]
            }
            
            results = list(self.container.query_items(
                query=query_spec["query"],
                parameters=query_spec["parameters"],
                enable_cross_partition_query=True
            ))
            
            # Format results
            formatted_results = [
                {
                    "content": item["content"],
                    "source": item["filename"],
                    "score": item.get("score", 0.0),
                    "metadata": item.get("metadata", {}),
                    "document_id": item["document_id"]
                }
                for item in results
            ]
            
            logger.info(f"Vector search returned {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in similarity search: {e}", exc_info=True)
            # Fallback to simple keyword search if vector search fails
            return await self._fallback_search(query, max_results)
    
    async def _fallback_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Fallback keyword-based search"""
        try:
            query_spec = {
                "query": "SELECT TOP @max_results * FROM c WHERE CONTAINS(c.content, @query)",
                "parameters": [
                    {"name": "@max_results", "value": max_results},
                    {"name": "@query", "value": query}
                ]
            }
            
            results = list(self.container.query_items(
                query=query_spec["query"],
                parameters=query_spec["parameters"],
                enable_cross_partition_query=True
            ))
            
            return [
                {
                    "content": item["content"],
                    "source": item["filename"],
                    "score": 0.5,  # Default score for keyword match
                    "metadata": item.get("metadata", {}),
                    "document_id": item["document_id"]
                }
                for item in results[:max_results]
            ]
        except Exception as e:
            logger.error(f"Fallback search failed: {e}")
            return []
    
    async def list_documents(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """List all documents in the store"""
        try:
            query = f"SELECT DISTINCT c.document_id, c.filename, c.metadata FROM c OFFSET {skip} LIMIT {limit}"
            results = list(self.container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            return results
        except Exception as e:
            logger.error(f"Error listing documents: {e}")
            return []
    
    async def delete_document(self, document_id: str):
        """Delete document and all its chunks"""
        try:
            query = "SELECT c.id, c.document_id FROM c WHERE c.document_id = @document_id"
            items = list(self.container.query_items(
                query=query,
                parameters=[{"name": "@document_id", "value": document_id}],
                enable_cross_partition_query=True
            ))
            
            for item in items:
                self.container.delete_item(item=item["id"], partition_key=document_id)
            
            logger.info(f"Deleted document {document_id} with {len(items)} chunks")
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            raise
    
    async def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Get document by ID"""
        try:
            query = "SELECT * FROM c WHERE c.document_id = @document_id"
            items = list(self.container.query_items(
                query=query,
                parameters=[{"name": "@document_id", "value": document_id}],
                enable_cross_partition_query=True
            ))
            
            if items:
                return {
                    "document_id": document_id,
                    "filename": items[0]["filename"],
                    "chunks": len(items),
                    "metadata": items[0].get("metadata", {})
                }
            return None
        except Exception as e:
            logger.error(f"Error getting document: {e}")
            return None
