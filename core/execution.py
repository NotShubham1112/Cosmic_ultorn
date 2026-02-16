import os
import subprocess
from typing import List
from rich.console import Console
from core.planner import Plan, Step
from core.tools.mcp.registry import ToolRegistry
from core.tools.mcp.schemas import ToolCall

console = Console()

class Executor:
    def __init__(self):
        self.registry = ToolRegistry()

    def execute_plan(self, plan: Plan) -> bool:
        """
        Executes a given plan step-by-step.
        Returns True if all steps succeed, False otherwise.
        """
        console.print(f"[bold]Executing Plan:[/bold] {plan.goal}")
        
        for step in plan.steps:
            console.print(f"\n[blue]Step {step.id}: {step.action} {step.path}[/blue]")
            console.print(f"  {step.description}")
            
            try:
                success = self._execute_step(step)
                if success:
                    step.status = "completed"
                    console.print(f"  [green][OK] Success[/green]")
                else:
                    step.status = "failed"
                    console.print(f"  [red][FAIL] Failed[/red]")
                    return False
            except Exception as e:
                step.status = "error"
                console.print(f"  [red][ERR] Error: {e}[/red]")
                return False
                
        return True

    def _execute_step(self, step: Step) -> bool:
        if step.action == "create":
            return self._create_file(step.path, step.content)
        elif step.action == "modify":
            return self._modify_file(step.path, step.content)
        elif step.action == "delete":
            return self._delete_file(step.path)
        elif step.action == "run_command":
            return self._run_command(step.path)
        elif step.action == "review":
            console.print("  [yellow]Manual review required. Skipping execution.[/yellow]")
            return True
        elif step.action == "tool_call":
            return self._execute_tool(step.tool_call)
        else:
            console.print(f"  [red]Unknown action: {step.action}[/red]")
            return False

    def _execute_tool(self, call: ToolCall) -> bool:
        if not call:
            console.print("  [red]Tool call missing details.[/red]")
            return False
            
        console.print(f"  [cyan]Calling Tool:[/cyan] {call.tool} Args: {call.args}")
        result = self.registry.execute_tool(call)
        
        if result.success:
            console.print(f"  [green]Result:[/green] {result.output}")
            return True
        else:
            console.print(f"  [red]Tool Error:[/red] {result.error} - {result.output}")
            return False

    def _create_file(self, path: str, content: str | None) -> bool:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content if content else "")
            return True
        except Exception as e:
            console.print(f"  [red]Create failed: {e}[/red]")
            return False

    def _modify_file(self, path: str, content: str | None) -> bool:
        """
        Simple overwrite modification. 
        TODO: Implement smart diff/patching.
        """
        if not os.path.exists(path):
            console.print(f"  [red]File not found: {path}[/red]")
            return False
        
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content if content else "")
            return True
        except Exception as e:
            console.print(f"  [red]Modify failed: {e}[/red]")
            return False

    def _delete_file(self, path: str) -> bool:
        try:
            if os.path.exists(path):
                os.remove(path)
            return True
        except Exception as e:
            console.print(f"  [red]Delete failed: {e}[/red]")
            return False

    def _run_command(self, command: str) -> bool:
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                console.print(f"  Output: {result.stdout.strip()}")
                return True
            else:
                console.print(f"  [red]Command failed:[/red] {result.stderr.strip()}")
                return False
        except Exception as e:
            console.print(f"  [red]Command execution error: {e}[/red]")
            return False
