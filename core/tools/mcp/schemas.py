from typing import List, Dict, Any, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field

class RiskLevel(str, Enum):
    SAFE = "safe"           # Read-only, non-sensitive (e.g., read_file, list_dir)
    LOW = "low"             # Minor changes, reversible (e.g., create_temp_file)
    MEDIUM = "medium"       # Significant changes (e.g., modify_code, create_pr)
    HIGH = "high"           # Destructive or costly (e.g., delete_file, deploy_prod)

class ToolArgument(BaseModel):
    name: str
    type: str
    description: str
    required: bool = True

class Tool(BaseModel):
    name: str
    description: str
    args_schema: Any  # JSON Schema or Pydantic model
    risk_level: RiskLevel = RiskLevel.MEDIUM
    
class ToolCall(BaseModel):
    tool: str
    args: Dict[str, Any]
    id: Optional[str] = None

class ToolResult(BaseModel):
    tool_call_id: Optional[str] = None
    output: Any
    error: Optional[str] = None
    success: bool = True

class MCPConfig(BaseModel):
    enabled_servers: List[str] = []
    local_servers: Dict[str, str] = {}  # name -> command
    remote_servers: Dict[str, str] = {} # name -> url
