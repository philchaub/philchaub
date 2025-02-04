# importation par default 
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.flow.flow import Flow, listen, start , or_

from pydantic import BaseModel
from typing import List


# Autre importation 
from src.megacrew.tools.custom_tool  import  MyCustomTool
from crewai.cli.constants import ENV_VARS

from src.megacrew.crew import conduct_research 




