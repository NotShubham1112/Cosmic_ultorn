import sys
import os

# Add parent dir to path to import core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.tools.mcp.registry import ToolRegistry
from core.tools.builtins.filesystem import create_filesystem_client
from core.tools.mcp.schemas import ToolCall

def test_mcp():
    print("Initializing Registry...")
    registry = ToolRegistry()
    
    # Manually register for test (normally Planner does this)
    print("Registering FileSystem...")
    fs_client = create_filesystem_client()
    registry.register_server("filesystem", fs_client)
    for tool in fs_client.list_tools():
        registry.register_tool("filesystem", tool)
        print(f"  Registered: {tool.name}")

    # Test List Tools
    tools = registry.list_tools()
    print(f"\nTotal Tools: {len(tools)}")
    
    # Test Execution (Safe)
    print("\nTesting 'fs_list_directory'...")
    call = ToolCall(tool="fs_list_directory", args={"path": "."})
    result = registry.execute_tool(call)
    print(f"Result success: {result.success}")
    print(f"Output: {result.output}")

    # Test Execution (Permission Check - Mock)
    # We didn't set up interactive permission manager, so it should fail if risk is high and we didn't confirm.
    # But fs_list_directory is likely SAFE or MEDIUM. 
    # Let's try writing a file (Method fs_write_file) - should be checked.
    
    print("\nTesting 'fs_write_file' (Should check permissions)...")
    call_write = ToolCall(tool="fs_write_file", args={"path": "test_mcp_output.txt", "content": "Hello MCP"})
    
    # Default permission manager might block it or allow it depending on defaults.
    # In my permission.py, I mostly set defaults. write_file is likely Medium risk (default).
    # PermissionsManager default says: defaults to MEDIUM.
    # defaults to MEDIUM -> requires confirmation (unless overridden).
    # Let's see what happens.
    
    result_write = registry.execute_tool(call_write)
    print(f"Write Result success: {result_write.success}")
    print(f"Write Output: {result_write.output}")

if __name__ == "__main__":
    test_mcp()
