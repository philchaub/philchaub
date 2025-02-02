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
        # rep = []
        # for a in answer.split("\n"):
        #     rep.append(a)
        return answer
    return _run(prompt)
    
        
class MyCustomTool(BaseTool):
    name: str = "API_manette_tools"
    description: str = " API to resquest answer about blender geometry nodes functionality."
    def _run(self, argument: str) -> str:
        print("argument",argument)
        return tool_wrapper(argument)   


