import os
import ast
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging
import networkx as nx
import json

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
        self.graph = nx.DiGraph()
        
    def walk_and_index(self):
        """Walks the repository and indexes supported files."""
        logger.info(f"Indexing repository at {self.root_path}")
        
        # 1. First pass: Parse all files
        for root, dirs, files in os.walk(self.root_path):
            if ".git" in dirs: dirs.remove(".git")
            if "node_modules" in dirs: dirs.remove("node_modules")
            if "__pycache__" in dirs: dirs.remove("__pycache__")
            if "venv" in dirs: dirs.remove("venv") 

            for file in files:
                file_path = Path(root) / file
                self._index_file(file_path)
        
        # 2. Second pass: Build Dependency Graph
        self._build_dependency_graph()
        
        logger.info(f"Indexed {len(self.index)} files. Graph has {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges.")

    def _index_file(self, file_path: Path):
        """Read and parse a single file."""
        if file_path.suffix == ".py":
            self._parse_python(file_path)

    def _parse_python(self, file_path: Path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            rel_path = str(file_path.relative_to(self.root_path)).replace("\\", "/")
            node = FileNode(rel_path, content, "python")
            
            tree = ast.parse(content)
            
            for item in ast.walk(tree):
                if isinstance(item, ast.FunctionDef):
                    node.functions.append({"name": item.name, "lineno": item.lineno})
                elif isinstance(item, ast.ClassDef):
                    node.classes.append({"name": item.name, "lineno": item.lineno})
                elif isinstance(item, ast.Import):
                    for name in item.names:
                        node.imports.append(name.name)
                elif isinstance(item, ast.ImportFrom):
                    module = item.module if item.module else ""
                    for name in item.names:
                        if module:
                            node.imports.append(f"{module}.{name.name}")
                        else:
                            node.imports.append(name.name)

            self.index[rel_path] = node

        except Exception as e:
            logger.error(f"Failed to parse {file_path}: {e}")

    def _build_dependency_graph(self):
        """Constructs a directed graph from imports."""
        for path, node in self.index.items():
            self.graph.add_node(path, type="file", lang=node.language)
            
            for imp in node.imports:
                # Try to resolve import to a file
                parts = imp.split(".")
                resolved = False
                
                # Check progressively shorter paths to find the module file
                # e.g. core.indexer.Indexer -> check core/indexer/Indexer.py, then core/indexer.py
                for i in range(len(parts), 0, -1):
                    # candidate path: core/indexer.py
                    candidate = "/".join(parts[:i]) + ".py"
                    if candidate in self.index:
                        self.graph.add_edge(path, candidate, type="import")
                        # print(f"DEBUG: Resolved {imp} -> {candidate}")
                        resolved = True
                        break
                    
                    # candidate package: core/indexer/__init__.py
                    candidate_init = "/".join(parts[:i]) + "/__init__.py"
                    if candidate_init in self.index:
                        self.graph.add_edge(path, candidate_init, type="import")
                        # print(f"DEBUG: Resolved {imp} -> {candidate_init}")
                        resolved = True
                        break
                
                # if not resolved:
                #    print(f"DEBUG: Could not resolve {imp}")

    def get_summary(self):
        summary = "Repository Summary:\n"
        summary += f"Total Files: {len(self.index)}\n"
        summary += f"Total Dependencies: {self.graph.number_of_edges()}\n"
        return summary
    
    def export_graph(self, output_path: str = "dependency_graph.json"):
        data = nx.node_link_data(self.graph)
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)
        return output_path

if __name__ == "__main__":
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    indexer = Indexer(root)
    indexer.walk_and_index()
    print(indexer.get_summary())
    indexer.export_graph()
    print("Graph exported to dependency_graph.json")
