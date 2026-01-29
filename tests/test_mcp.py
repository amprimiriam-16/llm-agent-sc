"""
Test MCP Server
"""
import pytest
from backend.mcp.server import MCPServer


def test_mcp_server_initialization():
    """Test MCP server initialization"""
    server = MCPServer()
    assert server is not None
    assert len(server.tools) > 0


def test_mcp_tool_list():
    """Test getting MCP tool list"""
    server = MCPServer()
    tools = server.get_tool_list()
    
    assert len(tools) > 0
    assert all("name" in tool for tool in tools)
    assert all("description" in tool for tool in tools)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
