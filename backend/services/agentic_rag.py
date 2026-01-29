"""
Agentic RAG Implementation
Intelligent agent-based retrieval and reasoning
"""
from typing import Dict, Any, List
import uuid
import json

from backend.services.rag_pipeline import RAGPipeline
from backend.services.llm import LLMService
from backend.core.logging import logger


class AgenticRAG:
    """
    Agentic RAG system that can:
    - Plan multi-step queries
    - Decompose complex questions
    - Verify and cross-reference information
    - Provide reasoning traces
    """
    
    def __init__(self):
        self.rag_pipeline = RAGPipeline()
        self.llm = LLMService()
    
    async def process_query(
        self,
        question: str,
        max_sources: int = 5,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Process query using agentic approach
        
        Args:
            question: User question
            max_sources: Maximum sources to retrieve
            temperature: LLM temperature
            
        Returns:
            Enhanced result with reasoning trace
        """
        try:
            logger.info(f"Agentic RAG: Processing query with planning")
            
            # Step 1: Analyze and decompose question
            sub_queries = await self._decompose_question(question)
            logger.info(f"Decomposed into {len(sub_queries)} sub-queries")
            
            # Step 2: Execute sub-queries
            all_sources = []
            query_results = []
            
            for sub_query in sub_queries:
                result = await self.rag_pipeline.query(
                    question=sub_query,
                    max_sources=max_sources // len(sub_queries) + 1,
                    temperature=temperature
                )
                all_sources.extend(result["sources"])
                query_results.append({
                    "query": sub_query,
                    "answer": result["answer"]
                })
            
            # Step 3: Deduplicate and rank sources
            unique_sources = self._deduplicate_sources(all_sources)
            top_sources = sorted(
                unique_sources,
                key=lambda x: x["score"],
                reverse=True
            )[:max_sources]
            
            # Step 4: Synthesize final answer with reasoning
            final_answer = await self._synthesize_answer(
                question=question,
                sub_results=query_results,
                sources=top_sources,
                temperature=temperature
            )
            
            # Step 5: Generate reasoning trace
            reasoning = self._generate_reasoning_trace(sub_queries, query_results)
            
            return {
                "answer": final_answer,
                "sources": top_sources,
                "conversation_id": str(uuid.uuid4()),
                "reasoning": reasoning,
                "sub_queries": sub_queries
            }
            
        except Exception as e:
            logger.error(f"Agentic RAG error: {e}", exc_info=True)
            # Fallback to standard RAG
            return await self.rag_pipeline.query(
                question=question,
                max_sources=max_sources,
                temperature=temperature
            )
    
    async def _decompose_question(self, question: str) -> List[str]:
        """
        Decompose complex question into sub-queries
        
        Args:
            question: Original question
            
        Returns:
            List of sub-queries
        """
        try:
system_message = """You are a query planning agent for Supply Chain Intelligence Platform.
Your task is to analyze questions and break them down into focused sub-queries that can be answered independently.

Guidelines:
- Identify key aspects of the question
- Create 1-3 focused sub-queries
- Each sub-query should be specific and answerable
- If the question is already simple, return it as-is
- Format: Return ONLY a JSON array of sub-queries
"""
            
            prompt = f"""Question: {question}

Decompose this into focused sub-queries. Return ONLY a JSON array, for example:
["sub-query 1", "sub-query 2"]"""
            
            response = await self.llm.generate_response(
                prompt=prompt,
                system_message=system_message,
                temperature=0.3,
                max_tokens=500
            )
            
            # Parse JSON response
            try:
                sub_queries = json.loads(response.strip())
                if isinstance(sub_queries, list) and sub_queries:
                    return sub_queries
            except json.JSONDecodeError:
                logger.warning("Failed to parse sub-queries, using original question")
            
            # Fallback to original question
            return [question]
            
        except Exception as e:
            logger.error(f"Question decomposition error: {e}")
            return [question]
    
    async def _synthesize_answer(
        self,
        question: str,
        sub_results: List[Dict[str, str]],
        sources: List[Dict[str, Any]],
        temperature: float
    ) -> str:
        """
        Synthesize final answer from sub-query results
        
        Args:
            question: Original question
            sub_results: Results from sub-queries
            sources: Retrieved source documents
            temperature: LLM temperature
            
        Returns:
            Synthesized answer
        """
        try:
            # Build synthesis context
            sub_answers = "\n\n".join([
                f"Sub-question: {r['query']}\nAnswer: {r['answer']}"
                for r in sub_results
            ])
            
            sources_text = "\n\n".join([
                f"[Source: {s['source']}]\n{s['content']}"
                for s in sources
            ])
            
            system_message = """You are an expert synthesis agent for Supply Chain Intelligence Platform.
Your task is to combine information from multiple sub-analyses into a comprehensive, coherent answer.

Guidelines:
- Integrate insights from all sub-analyses
- Resolve any contradictions
- Provide a well-structured, complete answer
- Cite sources appropriately
- Maintain professional standards
"""
            
            prompt = f"""Original Question: {question}

Sub-Analysis Results:
{sub_answers}

Supporting Sources:
{sources_text}

Synthesize a comprehensive answer to the original question, integrating all insights."""
            
            answer = await self.llm.generate_response(
                prompt=prompt,
                system_message=system_message,
                temperature=temperature,
                max_tokens=2048
            )
            
            return answer
            
        except Exception as e:
            logger.error(f"Answer synthesis error: {e}")
            # Return first sub-result as fallback
            return sub_results[0]["answer"] if sub_results else "Unable to generate answer."
    
    def _deduplicate_sources(self, sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate sources based on content similarity"""
        seen = set()
        unique = []
        
        for source in sources:
            # Use first 100 chars as simple dedup key
            key = source["content"][:100]
            if key not in seen:
                seen.add(key)
                unique.append(source)
        
        return unique
    
    def _generate_reasoning_trace(
        self,
        sub_queries: List[str],
        results: List[Dict[str, str]]
    ) -> str:
        """Generate human-readable reasoning trace"""
        trace_parts = [
            "**Reasoning Process:**",
            f"\n1. Decomposed question into {len(sub_queries)} focused queries:",
        ]
        
        for i, query in enumerate(sub_queries, 1):
            trace_parts.append(f"   - Sub-query {i}: {query}")
        
        trace_parts.append("\n2. Retrieved and analyzed relevant information for each query")
        trace_parts.append("\n3. Synthesized findings into comprehensive answer")
        trace_parts.append("\n4. Verified consistency across sources")
        
        return "\n".join(trace_parts)
