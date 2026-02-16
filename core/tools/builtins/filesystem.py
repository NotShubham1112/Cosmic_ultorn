import os
import pathlib
from typing import List, Optional
from ..mcp.client import LocalFunctionsClient

# Sandbox configuration
SANDBOX_ROOT = pathlib.Path(os.getcwd()).resolve()

def _is_safe_path(path_str: str) -> bool:
    try:
        path = (SANDBOX_ROOT / path_str).resolve()
        return path.is_relative_to(SANDBOX_ROOT)
    except Exception:
        return False

def read_file(path: str) -> str:
    """Reads a file from the sandbox."""
    if not _is_safe_path(path):
        raise PermissionError(f"Access denied: {path} is outside sandbox.")
    
    full_path = SANDBOX_ROOT / path
    if not full_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
        
    return full_path.read_text(encoding='utf-8')

def write_file(path: str, content: str) -> str:
    """Writes content to a file in the sandbox."""
    if not _is_safe_path(path):
         raise PermissionError(f"Access denied: {path} is outside sandbox.")
         
    full_path = SANDBOX_ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content, encoding='utf-8')
    return f"Successfully wrote to {path}"

def list_directory(path: str = ".") -> List[str]:
    """Lists contents of a directory in the sandbox."""
    if not _is_safe_path(path):
        raise PermissionError(f"Access denied: {path} is outside sandbox.")
        
    full_path = SANDBOX_ROOT / path
    if not full_path.exists() or not full_path.is_dir():
        raise NotADirectoryError(f"Directory not found: {path}")
        
    return [p.name for p in full_path.iterdir()]

def create_filesystem_client() -> LocalFunctionsClient:
    return LocalFunctionsClient(
        functions=[read_file, write_file, list_directory],
        name_prefix="fs_"
    )
