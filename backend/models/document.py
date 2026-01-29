"""
Document Models
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class Document(BaseModel):
    id: str
    filename: str
    content: str
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime] = None


class DocumentChunk(BaseModel):
    id: str
    document_id: str
    chunk_index: int
    content: str
    embedding: Optional[list] = None
    metadata: Dict[str, Any]
