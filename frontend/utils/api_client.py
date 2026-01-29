"""
API Client for Backend Communication
"""
import requests
from typing import Dict, Any, List, Optional
import os


class APIClient:
    """Client for communicating with FastAPI backend"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("API_BASE_URL", "http://localhost:8000")
    
    def ask_question(
        self,
        question: str,
        use_agentic: bool = True,
        max_sources: int = 5,
        temperature: float = 0.7,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Ask a question to the API
        
        Args:
            question: Question to ask
            use_agentic: Use agentic RAG
            max_sources: Maximum sources
            temperature: LLM temperature
            conversation_id: Conversation ID
            
        Returns:
            API response
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/chat/ask",
                json={
                    "question": question,
                    "use_agentic": use_agentic,
                    "max_sources": max_sources,
                    "temperature": temperature,
                    "conversation_id": conversation_id
                },
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return None
    
    def upload_documents(
        self,
        files: List[tuple],
        classification: str = "CONFIDENTIAL"
    ) -> Dict[str, Any]:
        """
        Upload documents to the API
        
        Args:
            files: List of file tuples
            classification: Data classification
            
        Returns:
            Upload response
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/documents/upload",
                files=files,
                data={"classification": classification},
                timeout=300
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Upload Error: {e}")
            return None
    
    def list_documents(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """List all documents"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/documents/list",
                params={"skip": skip, "limit": limit},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"List Error: {e}")
            return None
    
    def delete_document(self, document_id: str) -> Dict[str, Any]:
        """Delete a document"""
        try:
            response = requests.delete(
                f"{self.base_url}/api/v1/documents/{document_id}",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Delete Error: {e}")
            return None
    
    def get_health(self) -> Dict[str, Any]:
        """Get system health status"""
        try:
            response = requests.get(
                f"{self.base_url}/health",
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Health Check Error: {e}")
            return {"status": "unhealthy"}
