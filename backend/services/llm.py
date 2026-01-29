"""
LLM Service for Azure OpenAI
"""
from typing import List, Dict, Any, Optional
from openai import AzureOpenAI

from backend.core.config import settings
from backend.core.logging import logger


class LLMService:
    """Service for interacting with Azure OpenAI LLM"""
    
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
        )
        self.deployment = settings.AZURE_OPENAI_DEPLOYMENT_NAME
    
    async def generate_response(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        context: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generate response from LLM
        
        Args:
            prompt: User prompt
            system_message: System instruction
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            context: Previous conversation context
            
        Returns:
            Generated text response
        """
        try:
            messages = []
            
            # Add system message
            if system_message:
                messages.append({
                    "role": "system",
                    "content": system_message
                })
            
            # Add conversation context
            if context:
                messages.extend(context)
            
            # Add current prompt
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Call Azure OpenAI
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            answer = response.choices[0].message.content
            
            logger.info(
                f"Generated response: {len(answer)} chars, "
                f"tokens: {response.usage.total_tokens}"
            )
            
            return answer
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}", exc_info=True)
            raise
    
    async def generate_with_sources(
        self,
        question: str,
        sources: List[Dict[str, Any]],
        temperature: float = 0.7
    ) -> str:
        """
        Generate answer using retrieved sources (RAG)
        
        Args:
            question: User question
            sources: Retrieved source documents
            temperature: Sampling temperature
            
        Returns:
            Generated answer with source citations
        """
        try:
            # Build context from sources
            context_parts = []
            for i, source in enumerate(sources, 1):
                context_parts.append(
                    f"[Source {i}: {source['source']}]\n{source['content']}\n"
                )
            
            context_text = "\n".join(context_parts)
            
            # Create RAG prompt
system_message = """You are an expert AI assistant for Supply Chain Intelligence.
Your role is to provide accurate, well-sourced answers to questions about supply chain operations, 
procurement, logistics, and related topics.

Guidelines:
- Base your answers strictly on the provided sources
- Cite sources using [Source N] format
- If information is not in the sources, clearly state that
- Be concise but comprehensive
- Use domain-specific terminology appropriately
- Maintain professional standards and confidentiality
"""
            
            user_prompt = f"""Context from documents:

{context_text}

Question: {question}

Please provide a detailed answer based on the context above. Include source citations."""
            
            answer = await self.generate_response(
                prompt=user_prompt,
                system_message=system_message,
                temperature=temperature,
                max_tokens=settings.MAX_TOKENS
            )
            
            return answer
            
        except Exception as e:
            logger.error(f"Error in RAG generation: {e}", exc_info=True)
            raise
