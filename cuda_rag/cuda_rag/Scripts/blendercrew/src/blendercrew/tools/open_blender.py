

# script coté crewai
import subprocess
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from crewai.tools.structured_tool import CrewStructuredTool
from typing import Type,ClassVar
import requests
import json
import os

# Wrapper function to execute the API call
def tool_blender(prompt):#*args, **kwargs
    def _run(prompt: str) -> str:       
        sub = subprocess.Popen(prompt)
        sub.wait()
        answer = {}
        answerPath = "C:/Users/isisc/IA/cuda_rag/cuda_rag/Scripts/blendercrew/src/blendercrew/tools/blender_comm.json"
        if os.path.exists(answerPath):
            with open(answerPath, 'r') as f:
                answer = json.load(f)
        print("answer",answer)
        if "error" in answer:
            return answer["error"]
        else:
            return ["answer file missing error"]
    # sub = subprocess.Popen(
    #     prompt,
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.PIPE,
    #     stdin=subprocess.PIPE,
    #     encoding='utf-8'
    #     )
    return _run(prompt)
    
        
class ScriptTestTool(BaseTool):
    name: str = "scriptTest_tool"
    description: str = "tool to test a script."
    def _run(self, script: str) -> str:
        scriptPath = 'C:/Users/isisc/IA/cuda_rag/cuda_rag/Scripts/blendercrew/src/blendercrew/tools/testScript.py'
        print('argument',script)
        #argument = 'blender -b --python ' + 'C:/Users/isisc/IA/cuda_rag/cuda_rag/Scripts/blendercrew/src/blendercrew/tools/blender_comm.py' + ' scriptPath '+ scriptPath
        script = 'blender --python ' + 'C:/Users/isisc/IA/cuda_rag/cuda_rag/Scripts/blendercrew/src/blendercrew/tools/blender_comm.py' + ' scriptPath '+ scriptPath
        # C:/Program Files/Blender Foundation/Blender 4.3/blender-launcher.exe
        return tool_blender(script)   
  



