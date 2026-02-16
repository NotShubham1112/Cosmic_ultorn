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
from core.memory.persistence import Memory
from core.execution import Executor

app = typer.Typer(help="Cosmic Ultorn - AI Engineering OS CLI")
console = Console()
memory = Memory()

@app.command()
def index(path: str = typer.Argument(..., help="Path to the repository")):
    """
    Index a repository to build the knowledge graph and save to memory.
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
    
    memory.save_index(indexer)

@app.command()
def plan(goal: str = typer.Argument(..., help="The goal to achieve")):
    """
    Generate an implementation plan and save to memory.
    """
    console.print(f"[bold green]Planning goal:[/bold green] {goal}")
    planner = Planner()
    plan_obj = planner.create_plan(goal)
    console.print(f"[bold]Plan for:[/bold] {plan_obj.goal}")
    for step in plan_obj.steps:
        console.print(f"{step.id}. {step.action.upper()} {step.path} - {step.description}")
        
    memory.save_plan(plan_obj)

@app.command()
def execute():
    """
    Execute the last generated plan from memory.
    """
    plan_obj = memory.load_plan()
    if not plan_obj:
        console.print("[bold red]No plan found in memory. Run 'plan' first.[/bold red]")
        raise typer.Exit(code=1)
        
    executor = Executor()
    success = executor.execute_plan(plan_obj)
    
    if success:
        console.print("[bold green]Execution completed successfully![/bold green]")
    else:
        console.print("[bold red]Execution failed.[/bold red]")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
