import sys
import os
# Force add the user site-packages path where pip installs packages
# This is a workaround for the current environment setup
sys.path.append(os.path.expanduser("~\\AppData\\Roaming\\Python\\Python314\\site-packages"))

import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path
from core.indexer import Indexer
from core.planner import Planner

app = typer.Typer(help="Cosmic Ultorn - AI Engineering OS CLI")
console = Console()

@app.command()
def index(path: str = typer.Argument(..., help="Path to the repository")):
    """
    Index a repository to build the knowledge graph.
    """
    path_obj = Path(path)
    if not path_obj.exists():
        console.print(f"[bold red]Error:[/bold red] Path {path} does not exist.")
        raise typer.Exit(code=1)

    console.print(f"[bold blue]Indexing repository at:[/bold blue] {path}")
    
    indexer = Indexer(path)
    indexer.walk_and_index()
    
    summary = indexer.get_summary()
    console.print(summary)

@app.command()
def plan(goal: str = typer.Argument(..., help="The goal to achieve")):
    """
    Generate an implementation plan for a given goal.
    """
    console.print(f"[bold green]Planning goal:[/bold green] {goal}")
    planner = Planner()
    plan_obj = planner.create_plan(goal)
    console.print(f"[bold]Plan for:[/bold] {plan_obj.goal}")
    for step in plan_obj.steps:
        console.print(f"{step.id}. {step.description} [{step.status}]")

if __name__ == "__main__":
    app()
