import abc
import json
import subprocess
import requests
from typing import List, Dict, Any, Optional, Callable
from .schemas import Tool, ToolCall, ToolResult, ToolArgument, RiskLevel

class MCPClient(abc.ABC):
    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def list_tools(self) -> List[Tool]:
        pass

    @abc.abstractmethod
    def call_tool(self, call: ToolCall) -> ToolResult:
        pass

class StdioMCPClient(MCPClient):
    def __init__(self, command: str, args: List[str], env: Optional[Dict[str, str]] = None):
        self.command = command
        self.args = args
        self.env = env
        self.process = None

    def connect(self):
        # In a real implementation, this would start the subprocess and set up JSON-RPC communication
        # For now, we'll keep it as a placeholder for the connection logic
        pass

    def list_tools(self) -> List[Tool]:
        # Would send 'tools/list' request
        return []

    def call_tool(self, call: ToolCall) -> ToolResult:
        # Would send 'tools/call' request
        return ToolResult(output="Mock output from StdioMCPClient", success=True)

class HttpMCPClient(MCPClient):
    def __init__(self, url: str):
        self.url = url

    def connect(self):
        # Verify connection
        pass

    def list_tools(self) -> List[Tool]:
        # Would send GET /tools
        return []

    def call_tool(self, call: ToolCall) -> ToolResult:
        # Would send POST /tools/call
        return ToolResult(output="Mock output from HttpMCPClient", success=True)

class LocalFunctionsClient(MCPClient):
    """
    Exposes local python functions as MCP tools.
    """
    def __init__(self, functions: List[Callable], name_prefix: str = ""):
        self.functions = {f.__name__: f for f in functions}
        self.name_prefix = name_prefix

    def connect(self):
        pass

    def list_tools(self) -> List[Tool]:
        tools = []
        for name, func in self.functions.items():
            # In a real implementation, we would inspect type hints and docstrings
            # to generate the schema. For now, we use placeholders.
            tool_name = f"{self.name_prefix}{name}"
            tools.append(Tool(
                name=tool_name,
                description=func.__doc__ or "No description",
                args_schema={}, # Placeholder
                risk_level=RiskLevel.MEDIUM # Default
            ))
        return tools

    def call_tool(self, call: ToolCall) -> ToolResult:
        # Strip prefix if needed
        local_name = call.tool
        if self.name_prefix and local_name.startswith(self.name_prefix):
            local_name = local_name[len(self.name_prefix):]
            
        func = self.functions.get(local_name)
        if not func:
             return ToolResult(output=f"Function '{local_name}' not found", success=False, error="FunctionNotFound")
        
        try:
            result = func(**call.args)
            return ToolResult(output=result, success=True)
        except Exception as e:
            return ToolResult(output=str(e), success=False, error="ExecutionError")
