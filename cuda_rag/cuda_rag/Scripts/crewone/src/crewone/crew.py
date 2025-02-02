from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai_tools import SerperDevTool
from .tools import custom_tool

# for custom tools <with decorator
from typing import Type
import requests
from crewai.tools import tool

from crewai.cli.constants import ENV_VARSfo

# Override the key name dynamically
for entry in ENV_VARS.get("ollama", []):
    if "API_BASE" in entry:
        entry["BASE_URL"] = entry.pop("API_BASE")  # Rename the key


@CrewBase
class Crewone():
	"""Crewone crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'


	"""
	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True
		)

	
	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			output_file='output/report.md'
		)
	"""
	# MANETTE AGENT
	@agent
	def agent_manette(self) -> Agent:
		return Agent(
			config=self.agents_config['agent_manette'],
			verbose=True,
			tools=[custom_tool.MyCustomTool()]	
    		)

	@task
	def research_manette(self) -> Task: 
		return Task(
			config=self.tasks_config['research_manette'],
			async_execution=True,
			tools=[custom_tool.MyCustomTool()],
			)

	# CREW
	@crew
	def crew(self) -> Crew:
		"""Creates the Crewone crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)



