"""
MCP Protocol Handlers
"""
from typing import Dict, Any
import json


class MCPProtocol:
    """MCP Protocol implementation for standardized communication"""
    
    @staticmethod
    def create_request(
        method: str,
        params: Dict[str, Any],
        request_id: str = None
    ) -> str:
        """
        Create MCP request
        
        Args:
            method: Method name
            params: Parameters
            request_id: Optional request ID
            
        Returns:
            JSON-RPC formatted request
        """
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
        
        if request_id:
            request["id"] = request_id
        
        return json.dumps(request)
    
    @staticmethod
    def create_response(
        result: Any,
        request_id: str = None,
        error: Dict[str, Any] = None
    ) -> str:
        """
        Create MCP response
        
        Args:
            result: Result data
            request_id: Request ID
            error: Error information
            
        Returns:
            JSON-RPC formatted response
        """
        response = {
            "jsonrpc": "2.0"
        }
        
        if request_id:
            response["id"] = request_id
        
        if error:
            response["error"] = error
        else:
            response["result"] = result
        
        return json.dumps(response)
    
    @staticmethod
    def parse_request(message: str) -> Dict[str, Any]:
        """Parse MCP request"""
        try:
            data = json.loads(message)
            return {
                "method": data.get("method"),
                "params": data.get("params", {}),
                "id": data.get("id")
            }
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
    
    @staticmethod
    def parse_response(message: str) -> Dict[str, Any]:
        """Parse MCP response"""
        try:
            data = json.loads(message)
            return {
                "result": data.get("result"),
                "error": data.get("error"),
                "id": data.get("id")
            }
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
