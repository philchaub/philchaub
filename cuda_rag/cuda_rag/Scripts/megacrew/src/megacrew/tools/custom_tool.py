
#Template

#######################################################################################################################

# from crewai.tools import BaseTool
# from typing import Type
# from pydantic import BaseModel, Field


# class MyCustomToolInput(BaseModel):
#     """Input schema for MyCustomTool."""
#     argument: str = Field(..., description="Description of the argument.")

# class MyCustomTool(BaseTool):
#     name: str = "Name of my tool"
#     description: str = (
#         "Clear description for what this tool is useful for, your agent will need this information to use it."
#     )
#     args_schema: Type[BaseModel] = MyCustomToolInput

#     def _run(self, argument: str) -> str:
#         # Implementation goes here
#         return "this is an example of a tool output, ignore it and move along."

#######################################################################################################################

from crewai.tools import BaseTool
from crewai.tools.structured_tool import CrewStructuredTool
from typing import Type,ClassVar
from pydantic import BaseModel, Field
import requests


# Wrapper function to execute the API call
def tool_wrapper(prompt):#*args, **kwargs
    def _run(prompt: str) -> str:
        request = "crew"
        BASE_URL = "http://127.0.0.1:8000"
        print("prompt = ",prompt)
        response = requests.post(f"{BASE_URL}/{request}/?prompt={prompt}")
        answer = response.content.decode("utf-8")
        return answer
    return _run(prompt)
    
        
class MyCustomTool(BaseTool):
    name: str = "API_manette_tools"
    description: str = " API to resquest answer about blender geometry nodes functionality."
    def _run(self, argument: str) -> str:
        return tool_wrapper(argument)   



