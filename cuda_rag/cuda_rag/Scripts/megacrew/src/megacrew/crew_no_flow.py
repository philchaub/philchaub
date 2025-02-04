# importation par default 
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.flow.flow import Flow, listen, start

# Autre importation 
from src.megacrew.tools.custom_tool  import  MyCustomTool

from crewai.cli.constants import ENV_VARS

# Override the key name dynamically
for entry in ENV_VARS.get("ollama", []):
    if "API_BASE" in entry:
        entry["BASE_URL"] = entry.pop("API_BASE")  # Rename the key


@CrewBase
class Megacrew():
	"""Megacrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def tutor(self) -> Agent:
		return Agent(
			config=self.agents_config['tutor'],
			verbose=True,
			allow_delegation=True,
		)
	
	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			verbose=True,
			tools=[MyCustomTool()],
			allow_delegation=False,
		)



	@task
	def tutoring(self) -> Task:
		return Task(
			config=self.tasks_config['tutoring'],
			output_file='report.md'
		)
	
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_geometry_nodes'],
			tools=[MyCustomTool()]

		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Megacrew crew"""
		
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			#process=Process.sequential,
			process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
			manager_llm="ollama/mixtral",
			verbose=True,
			allow_delegation=True
		)
