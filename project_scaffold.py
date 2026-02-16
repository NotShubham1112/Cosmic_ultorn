import os
import pathlib

def create_structure():
    base_path = pathlib.Path("d:/Cosmic_ultorn")
    
    # Define the directory structure
    directories = [
        "core",                 # Python backend (AI Engine)
        "core/agents",          # Agent logic (Planner, coder, etc.)
        "core/memory",          # Vector DB & Graph interactions
        "core/tools",           # Tool definitions
        "desktop",              # Electron App
        "shared",               # Shared schemas/types
        "scripts",              # Dev ops scripts
        "docs",                 # Documentation
    ]
    
    # Create directories
    for dir_name in directories:
        dir_path = base_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        # Create __init__.py for python packages
        if dir_name.startswith("core") or dir_name == "scripts":
            (dir_path / "__init__.py").touch()
            
    print(f"Monorepo structure initialized at {base_path}")

if __name__ == "__main__":
    create_structure()
