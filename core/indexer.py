import os
import ast
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileNode:
    def __init__(self, path: str, content: str, language: str):
        self.path = path
        self.content = content
        self.language = language
        self.functions: List[Dict[str, Any]] = []
        self.classes: List[Dict[str, Any]] = []
        self.imports: List[str] = []

    def __repr__(self):
        return f"<FileNode path={self.path} lang={self.language}>"

class Indexer:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.index: Dict[str, FileNode] = {}
        
    def walk_and_index(self):
        """Walks the repository and indexes supported files."""
        logger.info(f"Indexing repository at {self.root_path}")
        
        for root, dirs, files in os.walk(self.root_path):
            # Skip hidden dirs and common excludes (basic implementation)
            if ".git" in dirs:
                dirs.remove(".git")
            if "node_modules" in dirs:
                dirs.remove("node_modules")
            if "__pycache__" in dirs:
                dirs.remove("__pycache__")
            if "venv" in dirs:
                dirs.remove("venv") 

            for file in files:
                file_path = Path(root) / file
                self._index_file(file_path)
        
        logger.info(f"Indexed {len(self.index)} files.")

    def _index_file(self, file_path: Path):
        """Read and parse a single file."""
        if file_path.suffix == ".py":
            self._parse_python(file_path)
        # Add more languages here (JS/TS, etc.)
        
    def _parse_python(self, file_path: Path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            node = FileNode(str(file_path.relative_to(self.root_path)), content, "python")
            
            # Use AST for Python
            tree = ast.parse(content)
            
            for item in ast.walk(tree):
                if isinstance(item, ast.FunctionDef):
                    node.functions.append({
                        "name": item.name,
                        "lineno": item.lineno,
                        "args": [a.arg for a in item.args.args]
                    })
                elif isinstance(item, ast.ClassDef):
                    node.classes.append({
                        "name": item.name,
                        "lineno": item.lineno
                    })
                elif isinstance(item, ast.Import):
                    for name in item.names:
                        node.imports.append(name.name)
                elif isinstance(item, ast.ImportFrom):
                    module = item.module if item.module else ""
                    for name in item.names:
                        node.imports.append(f"{module}.{name.name}")

            self.index[str(file_path)] = node

        except Exception as e:
            logger.error(f"Failed to parse {file_path}: {e}")

    def get_summary(self):
        summary = "Repository Summary:\n"
        for path, node in self.index.items():
            summary += f"- {node.path}: {len(node.functions)} functions, {len(node.classes)} classes\n"
        return summary

if __name__ == "__main__":
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    indexer = Indexer(root)
    indexer.walk_and_index()
    print(indexer.get_summary())
