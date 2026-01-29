"""
Document Management Routes
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import List
from pydantic import BaseModel
import tempfile
import os

from backend.core.logging import logger
from backend.services.vector_store import CosmosDBVectorStore
from backend.services.embeddings import EmbeddingService

router = APIRouter()


class DocumentMetadata(BaseModel):
    id: str
    filename: str
    size: int
    content_type: str
    uploaded_at: str
    classification: str
    chunk_count: int


class UploadResponse(BaseModel):
    success: bool
    documents: List[DocumentMetadata]
    message: str


@router.post("/upload", response_model=UploadResponse)
async def upload_documents(
    files: List[UploadFile] = File(...),
    classification: str = Form("CONFIDENTIAL")
):
    """
    Upload and process documents for indexing
    """
    try:
        logger.info(f"Uploading {len(files)} documents")
        
        vector_store = CosmosDBVectorStore()
        embedding_service = EmbeddingService()
        processed_docs = []
        
        for file in files:
            # Save temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
                content = await file.read()
                tmp.write(content)
                tmp_path = tmp.name
            
            try:
                # Process document
                doc_id = await vector_store.add_document(
                    file_path=tmp_path,
                    filename=file.filename,
                    metadata={
                        "classification": classification,
                        "content_type": file.content_type,
                        "size": len(content)
                    }
                )
                
                processed_docs.append(DocumentMetadata(
                    id=doc_id,
                    filename=file.filename,
                    size=len(content),
                    content_type=file.content_type or "application/octet-stream",
                    uploaded_at="2026-01-29T00:00:00Z",
                    classification=classification,
                    chunk_count=0  # Update after chunking
                ))
                
            finally:
                os.unlink(tmp_path)
        
        return UploadResponse(
            success=True,
            documents=processed_docs,
            message=f"Successfully processed {len(processed_docs)} documents"
        )
        
    except Exception as e:
        logger.error(f"Error uploading documents: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def list_documents(skip: int = 0, limit: int = 100):
    """List all indexed documents"""
    try:
        vector_store = CosmosDBVectorStore()
        documents = await vector_store.list_documents(skip=skip, limit=limit)
        return {"documents": documents, "total": len(documents)}
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """Delete a document from the index"""
    try:
        vector_store = CosmosDBVectorStore()
        await vector_store.delete_document(document_id)
        return {"status": "deleted", "document_id": document_id}
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{document_id}")
async def get_document(document_id: str):
    """Get document details"""
    try:
        vector_store = CosmosDBVectorStore()
        document = await vector_store.get_document(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving document: {e}")
        raise HTTPException(status_code=500, detail=str(e))
