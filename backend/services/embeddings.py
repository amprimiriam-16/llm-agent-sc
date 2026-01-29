"""
Azure OpenAI Embedding Service
"""
from typing import List
from openai import AzureOpenAI

from backend.core.config import settings
from backend.core.logging import logger


class EmbeddingService:
    """Service for generating text embeddings using Azure OpenAI"""
    
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
        )
        self.deployment = settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT
    
    async def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Input text to embed
            
        Returns:
            Embedding vector
        """
        try:
            # Clean text
            text = text.replace("\n", " ").strip()
            
            if not text:
                logger.warning("Empty text provided for embedding")
                return [0.0] * 1536  # Return zero vector
            
            # Generate embedding
            response = self.client.embeddings.create(
                input=text,
                model=self.deployment
            )
            
            embedding = response.data[0].embedding
            logger.debug(f"Generated embedding of dimension {len(embedding)}")
            
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating embedding: {e}", exc_info=True)
            raise
    
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            # Clean texts
            cleaned_texts = [text.replace("\n", " ").strip() for text in texts]
            cleaned_texts = [text if text else " " for text in cleaned_texts]
            
            # Batch embedding
            response = self.client.embeddings.create(
                input=cleaned_texts,
                model=self.deployment
            )
            
            embeddings = [item.embedding for item in response.data]
            logger.info(f"Generated {len(embeddings)} embeddings")
            
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}", exc_info=True)
            raise
