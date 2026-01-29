"""
Response Models
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class SourceDocument(BaseModel):
    content: str
    source: str
    score: float
    metadata: Dict[str, Any]


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceDocument]
    conversation_id: str
    processing_time: float
    model_used: str
    agent_reasoning: Optional[str] = None
