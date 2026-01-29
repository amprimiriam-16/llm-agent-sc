"""
Query Models
"""
from pydantic import BaseModel
from typing import Optional


class Query(BaseModel):
    question: str
    use_agentic: bool = True
    max_sources: int = 5
    temperature: Optional[float] = 0.7
    conversation_id: Optional[str] = None
