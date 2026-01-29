"""
MCP (Model Context Protocol) Server Implementation
Provides standardized tools for LLM interactions
"""
import asyncio
import json
from typing import Dict, Any, List
from datetime import datetime

from backend.core.config import settings
from backend.core.logging import logger
from backend.services.vector_store import CosmosDBVectorStore
from backend.services.llm import LLMService


class MCPServer:
    """
    MCP Server implementation providing standardized tools:
    - search_documents: Semantic search
    - retrieve_context: Get relevant context
    - analyze_supply_chain: Domain-specific analysis
    - generate_insights: AI-powered insights
    """
    
    def __init__(self):
        self.vector_store = CosmosDBVectorStore()
        self.llm = LLMService()
        self.tools = self._register_tools()
    
    def _register_tools(self) -> Dict[str, Dict[str, Any]]:
        """Register available MCP tools"""
        return {
            "search_documents": {
                "description": "Search SCIP documents using semantic similarity",
                "parameters": {
                    "query": {"type": "string", "description": "Search query"},
                    "max_results": {"type": "integer", "default": 5}
                },
                "handler": self.search_documents
            },
            "retrieve_context": {
                "description": "Retrieve relevant context for a specific topic",
                "parameters": {
                    "topic": {"type": "string", "description": "Topic to get context for"},
                    "depth": {"type": "string", "enum": ["shallow", "medium", "deep"], "default": "medium"}
                },
                "handler": self.retrieve_context
            },
            "analyze_supply_chain": {
                "description": "Perform domain-specific supply chain analysis",
                "parameters": {
                    "query": {"type": "string", "description": "Analysis query"},
                    "focus_areas": {"type": "array", "items": {"type": "string"}}
                },
                "handler": self.analyze_supply_chain
            },
            "generate_insights": {
                "description": "Generate AI-powered insights from data",
                "parameters": {
                    "context": {"type": "string", "description": "Context for insight generation"},
                    "insight_type": {"type": "string", "enum": ["trends", "risks", "opportunities"]}
                },
                "handler": self.generate_insights
            }
        }
    
    async def search_documents(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        MCP Tool: Search documents
        
        Args:
            query: Search query
            max_results: Maximum results to return
            
        Returns:
            Search results with metadata
        """
        try:
            logger.info(f"MCP Tool: search_documents - query: {query}")
            
            results = await self.vector_store.similarity_search(
                query=query,
                max_results=max_results
            )
            
            return {
                "status": "success",
                "tool": "search_documents",
                "timestamp": datetime.utcnow().isoformat(),
                "results": results,
                "count": len(results)
            }
        except Exception as e:
            logger.error(f"MCP search_documents error: {e}")
            return {"status": "error", "error": str(e)}
    
    async def retrieve_context(self, topic: str, depth: str = "medium") -> Dict[str, Any]:
        """
        MCP Tool: Retrieve context
        
        Args:
            topic: Topic to retrieve context for
            depth: Context depth (shallow, medium, deep)
            
        Returns:
            Retrieved context
        """
        try:
            logger.info(f"MCP Tool: retrieve_context - topic: {topic}, depth: {depth}")
            
            # Map depth to max results
            depth_map = {"shallow": 3, "medium": 5, "deep": 10}
            max_results = depth_map.get(depth, 5)
            
            results = await self.vector_store.similarity_search(
                query=topic,
                max_results=max_results
            )
            
            # Aggregate context
            context = "\n\n".join([r["content"] for r in results])
            
            return {
                "status": "success",
                "tool": "retrieve_context",
                "timestamp": datetime.utcnow().isoformat(),
                "topic": topic,
                "depth": depth,
                "context": context,
                "source_count": len(results)
            }
        except Exception as e:
            logger.error(f"MCP retrieve_context error: {e}")
            return {"status": "error", "error": str(e)}
    
    async def analyze_supply_chain(
        self,
        query: str,
        focus_areas: List[str] = None
    ) -> Dict[str, Any]:
        """
        MCP Tool: Supply chain analysis
        
        Args:
            query: Analysis query
            focus_areas: Specific areas to focus on
            
        Returns:
            Analysis results
        """
        try:
            logger.info(f"MCP Tool: analyze_supply_chain - query: {query}")
            
            # Retrieve relevant data
            results = await self.vector_store.similarity_search(
                query=query,
                max_results=7
            )
            
            # Prepare analysis context
            context = "\n\n".join([r["content"] for r in results])
            
            # Generate analysis
            system_message = """You are a BASF supply chain analysis expert.
Provide structured, data-driven analysis focusing on:
- Key metrics and KPIs
- Risk assessment
- Optimization opportunities
- Actionable recommendations
"""
            
            analysis_prompt = f"""Supply Chain Analysis Request:
Query: {query}
Focus Areas: {', '.join(focus_areas) if focus_areas else 'General'}

Relevant Data:
{context}

Provide a structured analysis with clear insights and recommendations."""
            
            analysis = await self.llm.generate_response(
                prompt=analysis_prompt,
                system_message=system_message,
                temperature=0.5
            )
            
            return {
                "status": "success",
                "tool": "analyze_supply_chain",
                "timestamp": datetime.utcnow().isoformat(),
                "query": query,
                "focus_areas": focus_areas or [],
                "analysis": analysis,
                "sources_analyzed": len(results)
            }
        except Exception as e:
            logger.error(f"MCP analyze_supply_chain error: {e}")
            return {"status": "error", "error": str(e)}
    
    async def generate_insights(
        self,
        context: str,
        insight_type: str = "trends"
    ) -> Dict[str, Any]:
        """
        MCP Tool: Generate insights
        
        Args:
            context: Context for insight generation
            insight_type: Type of insights (trends, risks, opportunities)
            
        Returns:
            Generated insights
        """
        try:
            logger.info(f"MCP Tool: generate_insights - type: {insight_type}")
            
            insight_prompts = {
                "trends": "Identify and analyze emerging trends in the following context:",
                "risks": "Identify potential risks and mitigation strategies in the following context:",
                "opportunities": "Identify optimization opportunities and potential improvements in the following context:"
            }
            
            system_message = f"""You are a BASF strategic insights analyst.
Generate {insight_type} insights that are:
- Data-driven and specific
- Actionable with clear next steps
- Aligned with BASF operational excellence
"""
            
            prompt = f"""{insight_prompts.get(insight_type, insight_prompts['trends'])}

Context:
{context}

Provide 3-5 key insights with supporting evidence."""
            
            insights = await self.llm.generate_response(
                prompt=prompt,
                system_message=system_message,
                temperature=0.6
            )
            
            return {
                "status": "success",
                "tool": "generate_insights",
                "timestamp": datetime.utcnow().isoformat(),
                "insight_type": insight_type,
                "insights": insights
            }
        except Exception as e:
            logger.error(f"MCP generate_insights error: {e}")
            return {"status": "error", "error": str(e)}
    
    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an MCP tool
        
        Args:
            tool_name: Name of tool to execute
            parameters: Tool parameters
            
        Returns:
            Tool execution result
        """
        if tool_name not in self.tools:
            return {
                "status": "error",
                "error": f"Unknown tool: {tool_name}",
                "available_tools": list(self.tools.keys())
            }
        
        tool = self.tools[tool_name]
        handler = tool["handler"]
        
        try:
            result = await handler(**parameters)
            return result
        except Exception as e:
            logger.error(f"MCP tool execution error: {e}")
            return {"status": "error", "error": str(e)}
    
    def get_tool_list(self) -> List[Dict[str, Any]]:
        """Get list of available tools with descriptions"""
        return [
            {
                "name": name,
                "description": tool["description"],
                "parameters": tool["parameters"]
            }
            for name, tool in self.tools.items()
        ]


async def start_mcp_server():
    """Start MCP server (for standalone execution)"""
    logger.info(f"Starting MCP Server on port {settings.MCP_SERVER_PORT}")
    server = MCPServer()
    
    # Log available tools
    tools = server.get_tool_list()
    logger.info(f"Registered {len(tools)} MCP tools:")
    for tool in tools:
        logger.info(f"  - {tool['name']}: {tool['description']}")
    
    # Keep server running
    logger.info("MCP Server ready")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("MCP Server shutting down")


if __name__ == "__main__":
    asyncio.run(start_mcp_server())
