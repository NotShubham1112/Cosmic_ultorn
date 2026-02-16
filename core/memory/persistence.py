import json
import networkx as nx
from pathlib import Path
from typing import Dict, Optional, Any
from core.indexer import FileNode, Indexer
from core.planner import Plan, Step

class Memory:
    def __init__(self, base_path: str = ".cosmic_memory"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        self.index_path = self.base_path / "index.json"
        self.graph_path = self.base_path / "graph.json"
        self.plan_path = self.base_path / "plan.json"

    def save_index(self, indexer: Indexer):
        """Saves the index and graph to disk."""
        # Convert FileNode objects to dicts
        index_data = {}
        for path, node in indexer.index.items():
            index_data[path] = {
                "path": node.path,
                "language": node.language,
                "functions": node.functions,
                "classes": node.classes,
                "imports": node.imports
            }
        
        with open(self.index_path, "w") as f:
            json.dump(index_data, f, indent=2)
            
        # Save Graph
        graph_data = nx.node_link_data(indexer.graph)
        with open(self.graph_path, "w") as f:
            json.dump(graph_data, f, indent=2)
            
        print(f"[Memory] Saved index to {self.index_path}")

    def load_index(self, indexer: Indexer) -> bool:
        """Loads index and graph into the indexer instance."""
        if not self.index_path.exists():
            return False
            
        try:
            with open(self.index_path, "r") as f:
                index_data = json.load(f)
            
            for path, data in index_data.items():
                node = FileNode(data["path"], "", data["language"]) # Content not persisted for now
                node.functions = data.get("functions", [])
                node.classes = data.get("classes", [])
                node.imports = data.get("imports", [])
                indexer.index[path] = node
                
            if self.graph_path.exists():
                with open(self.graph_path, "r") as f:
                    graph_data = json.load(f)
                indexer.graph = nx.node_link_graph(graph_data)
                
            return True
        except Exception as e:
            print(f"[Memory] Failed to load index: {e}")
            return False

    def save_plan(self, plan: Plan):
        """Saves the current plan to disk."""
        with open(self.plan_path, "w") as f:
            json.dump(plan.model_dump(), f, indent=2)
        print(f"[Memory] Saved plan to {self.plan_path}")

    def load_plan(self) -> Optional[Plan]:
        """Loads the last plan from disk."""
        if not self.plan_path.exists():
            return None
            
        try:
            with open(self.plan_path, "r") as f:
                data = json.load(f)
            return Plan(**data)
        except Exception as e:
            print(f"[Memory] Failed to load plan: {e}")
            return None
