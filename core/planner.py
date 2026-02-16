from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from .tools.mcp.registry import ToolRegistry
from .tools.builtins.filesystem import create_filesystem_client
from .tools.integrations.github import GitHubMCPClient
from .tools.mcp.schemas import ToolCall

load_dotenv()

class Step(BaseModel):
    id: int
    action: str = "review" # create, modify, delete, run_command, review, tool_call
    path: str = ""
    description: str
    content: Optional[str] = None # New content for create/modify
    tool_call: Optional[ToolCall] = None # Structured tool call
    status: str = "pending"

class Plan(BaseModel):
    goal: str
    steps: List[Step]

class Planner:
    def __init__(self):
        self.registry = ToolRegistry()
        self._register_default_tools()

    def _register_default_tools(self):
        # 1. FileSystem (sandboxed)
        fs_client = create_filesystem_client()
        self.registry.register_server("filesystem", fs_client)
        for tool in fs_client.list_tools():
            self.registry.register_tool("filesystem", tool)

        # 2. GitHub
        gh_client = GitHubMCPClient()
        self.registry.register_server("github", gh_client)
        for tool in gh_client.list_tools():
            self.registry.register_tool("github", tool)

    def create_plan(self, goal: str) -> Plan:
        """
        Generates a plan for the given goal using an LLM if available, otherwise returns a mock.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        
        if api_key and api_key.startswith("sk-"):
            try:
                llm = ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=0)
                parser = PydanticOutputParser(pydantic_object=Plan)
                
                tools_desc = "\n".join([f"- {t.name}: {t.description}" for t in self.registry.list_tools()])
                
                system_prompt = f"""You are an expert AI software architect.
                Create a detailed, step-by-step implementation plan.
                
                Available Tools:
                {tools_desc}
                
                For each step, specify:
                - action: 'tool_call' (PREFERRED) or legacy actions ('create', 'modify', 'run_command')
                - tool_call: If action is 'tool_call', provide the tool name and arguments.
                - description: brief explanation of what to do
                
                Ensure dependencies are handled first.
                """
                
                prompt = ChatPromptTemplate.from_messages([
                    ("system", system_prompt),
                    ("user", "{goal}\n\n{format_instructions}")
                ])
                
                chain = prompt | llm | parser
                return chain.invoke({"goal": goal, "format_instructions": parser.get_format_instructions()})
            except Exception as e:
                print(f"[Warning] LLM planning failed: {e}. Falling back to mock.")
        else:
            print("[Info] No OpenAI API key found. Using mock planner.")

        # Mock Plan Fallback (Safe for testing)
        mock_steps = [
            Step(id=1, action="create", path="core/test_mock.py", content="print('Hello form Mock Planner')", description="Create a test file"),
            Step(id=2, action="run_command", path="echo 'Mock execution running'", description="Run a safe command"),
        ]
        
        return Plan(goal=goal, steps=mock_steps)
