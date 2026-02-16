from typing import Dict, List, Optional
from .schemas import Tool, ToolCall, ToolResult
from .client import MCPClient
from .permissions import PermissionManager

class ToolRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.clients: Dict[str, MCPClient] = {} # server_name -> client
        self.tools: Dict[str, Tool] = {}        # tool_name -> tool_def
        self.tool_to_server: Dict[str, str] = {} # tool_name -> server_name
        self.permission_manager = PermissionManager()
        self._initialized = True

    def register_server(self, name: str, client: MCPClient):
        self.clients[name] = client
        # In a real scenario, we would automatically discover tools here
        # tools = client.list_tools()
        # for tool in tools:
        #     self.register_tool(name, tool)

    def register_tool(self, server_name: str, tool: Tool):
        self.tools[tool.name] = tool
        self.tool_to_server[tool.name] = server_name

    def get_tool(self, name: str) -> Optional[Tool]:
        return self.tools.get(name)
    
    def list_tools(self) -> List[Tool]:
        return list(self.tools.values())

    def execute_tool(self, call: ToolCall) -> ToolResult:
        """
        Executes a tool call through the appropriate client, enforcing permissions.
        """
        tool_name = call.tool
        tool_def = self.get_tool(tool_name)
        
        if not tool_def:
            return ToolResult(output=f"Tool '{tool_name}' not found.", success=False, error="ToolNotFound")
            
        # 1. Permission Check
        if not self.permission_manager.check_permission(tool_def, call):
             # In a real CLI/GUI app, we would prompt the user here.
             # For now, we fail if it requires confirmation and we act autonomously.
             return ToolResult(
                 output=f"Tool '{tool_name}' requires user confirmation. Execution stopped.",
                 success=False,
                 error="PermissionDenied"
             )

        # 2. Routing
        server_name = self.tool_to_server.get(tool_name)
        if not server_name:
             return ToolResult(output=f"No server found for tool '{tool_name}'", success=False, error="ServerNotFound")
             
        client = self.clients.get(server_name)
        if not client:
             return ToolResult(output=f"Client for server '{server_name}' not found", success=False, error="ClientNotFound")
             
        # 3. Execution
        try:
            return client.call_tool(call)
        except Exception as e:
            return ToolResult(output=str(e), success=False, error="ExecutionError")
