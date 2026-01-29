"""
Chat and Q&A Routes
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel

from backend.core.logging import logger
from backend.services.rag_pipeline import RAGPipeline
from backend.services.agentic_rag import AgenticRAG
from backend.core.config import settings

router = APIRouter()


class QuestionRequest(BaseModel):
    question: str
    use_agentic: bool = True
    max_sources: int = 5
    temperature: Optional[float] = None
    conversation_id: Optional[str] = None


class SourceDocument(BaseModel):
    content: str
    source: str
    score: float
    metadata: dict


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceDocument]
    conversation_id: str
    processing_time: float
    model_used: str
    agent_reasoning: Optional[str] = None


@router.post("/ask", response_model=ChatResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question and get an AI-powered answer with sources
    """
    try:
        logger.info(f"Processing question: {request.question[:100]}...")
        
        import time
        start_time = time.time()
        
        # Initialize appropriate RAG system
        if request.use_agentic:
            rag_system = AgenticRAG()
            result = await rag_system.process_query(
                question=request.question,
                max_sources=request.max_sources,
                temperature=request.temperature or settings.TEMPERATURE
            )
            agent_reasoning = result.get("reasoning", None)
        else:
            rag_system = RAGPipeline()
            result = await rag_system.query(
                question=request.question,
                max_sources=request.max_sources,
                temperature=request.temperature or settings.TEMPERATURE
            )
            agent_reasoning = None
        
        processing_time = time.time() - start_time
        
        # Format sources
        sources = [
            SourceDocument(
                content=doc["content"],
                source=doc["source"],
                score=doc["score"],
                metadata=doc.get("metadata", {})
            )
            for doc in result.get("sources", [])
        ]
        
        response = ChatResponse(
            answer=result["answer"],
            sources=sources,
            conversation_id=request.conversation_id or result.get("conversation_id", "new"),
            processing_time=processing_time,
            model_used=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
            agent_reasoning=agent_reasoning
        )
        
        logger.info(f"Question processed successfully in {processing_time:.2f}s")
        return response
        
    except Exception as e:
        logger.error(f"Error processing question: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{conversation_id}")
async def get_conversation_history(conversation_id: str):
    """Get conversation history"""
    # Placeholder - implement conversation storage
    return {
        "conversation_id": conversation_id,
        "messages": []
    }


@router.delete("/history/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete conversation history"""
    return {"status": "deleted", "conversation_id": conversation_id}
