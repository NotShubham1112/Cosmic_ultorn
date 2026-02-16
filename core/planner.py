from typing import List, Dict, Any
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

class Step(BaseModel):
    id: int
    description: str
    status: str = "pending"

class Plan(BaseModel):
    goal: str
    steps: List[Step]

class Planner:
    def __init__(self):
        pass


    def create_plan(self, goal: str) -> Plan:
        """
        Generates a plan for the given goal using an LLM if available, otherwise returns a mock.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        
        if api_key and api_key.startswith("sk-"):
            try:
                llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
                parser = PydanticOutputParser(pydantic_object=Plan)
                
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are an expert software architect. Create a detailed implementation plan with steps."),
                    ("user", "{goal}\n\n{format_instructions}")
                ])
                
                chain = prompt | llm | parser
                return chain.invoke({"goal": goal, "format_instructions": parser.get_format_instructions()})
            except Exception as e:
                print(f"[Warning] LLM planning failed: {e}. Falling back to mock.")
        else:
            print("[Info] No OpenAI API key found. Using mock planner.")

        # Mock Plan Fallback
        mock_steps = [
            Step(id=1, description="Analyze the request (Mock Step)"),
            Step(id=2, description="Identify relevant files (Mock Step)"),
            Step(id=3, description="Propose changes (Mock Step)"),
            Step(id=4, description="Verify changes (Mock Step)")
        ]
        
        return Plan(goal=goal, steps=mock_steps)
