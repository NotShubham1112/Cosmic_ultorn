import sys
import json
import os
from pathlib import Path

# Add project root to path to import indexer
sys.path.append(str(Path(__file__).parent.parent.parent))
from core.indexer import Indexer

def main():
    indexer = None
    
    for line in sys.stdin:
        try:
            request = json.loads(line)
            method = request.get("method")
            req_id = request.get("id")
            params = request.get("params", {})
            
            if method == "list_tools":
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": [
                        {
                            "name": "indexer_scan",
                            "description": "Scan and index the repository codebase",
                            "args_schema": {
                                "type": "object",
                                "properties": {
                                    "path": {"type": "string", "description": "Root path to scan"}
                                },
                                "required": ["path"]
                            },
                            "risk_level": "safe"
                        },
                        {
                            "name": "indexer_summary",
                            "description": "Get a summary of the current index",
                            "args_schema": {"type": "object", "properties": {}},
                            "risk_level": "safe"
                        }
                    ]
                }
            elif method == "call_tool":
                name = params.get("name")
                args = params.get("arguments", {})
                
                if name == "indexer_scan":
                    scan_path = args.get("path", ".")
                    indexer = Indexer(scan_path)
                    indexer.walk_and_index()
                    result = indexer.get_summary()
                elif name == "indexer_summary":
                    if indexer:
                        result = indexer.get_summary()
                    else:
                        result = "No scan performed yet."
                else:
                    result = f"Tool {name} not found"
                
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": result
                }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": "Method not found"}
                }
            
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error Indexer MCP: {str(e)}\n")
            sys.stderr.flush()

if __name__ == "__main__":
    main()
