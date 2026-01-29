"""
RAG Pipeline Implementation
Orchestrates retrieval and generation
"""
from typing import Dict, Any, List
import uuid

from backend.services.vector_store import CosmosDBVectorStore
from backend.services.llm import LLMService
from backend.core.logging import logger
from backend.core.config import settings


class RAGPipeline:
    """Retrieval Augmented Generation Pipeline"""
    
    def __init__(self):
        self.vector_store = CosmosDBVectorStore()
        self.llm = LLMService()
    
    async def query(
        self,
        question: str,
        max_sources: int = 5,
        temperature: float = 0.7,
        min_score: float = 0.7
    ) -> Dict[str, Any]:
        """
        Process a query through the RAG pipeline
        
        Args:
            question: User question
            max_sources: Maximum number of source documents
            temperature: LLM temperature
            min_score: Minimum relevance score
            
        Returns:
            Dict with answer and sources
        """
        try:
            logger.info(f"RAG Pipeline: Processing query")
            
            # Step 1: Retrieve relevant documents
            sources = await self.vector_store.similarity_search(
                query=question,
                max_results=max_sources,
                min_score=min_score
            )
            
            if not sources:
                logger.warning("No relevant sources found")
                return {
                    "answer": "I don't have enough information in the knowledge base to answer this question. Please try rephrasing or ask about topics covered in the documentation.",
                    "sources": [],
                    "conversation_id": str(uuid.uuid4())
                }
            
            logger.info(f"Retrieved {len(sources)} relevant sources")
            
            # Step 2: Generate answer using LLM
            answer = await self.llm.generate_with_sources(
                question=question,
                sources=sources,
                temperature=temperature
            )
            
            # Step 3: Return results
            return {
                "answer": answer,
                "sources": sources,
                "conversation_id": str(uuid.uuid4())
            }
            
        except Exception as e:
            logger.error(f"RAG Pipeline error: {e}", exc_info=True)
            raise
    
    async def multi_query(
        self,
        questions: List[str],
        max_sources_per_query: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Process multiple queries (for agentic use)
        
        Args:
            questions: List of questions
            max_sources_per_query: Max sources per question
            
        Returns:
            List of query results
        """
        results = []
        for question in questions:
            result = await self.query(
                question=question,
                max_sources=max_sources_per_query
            )
            results.append(result)
        return results
