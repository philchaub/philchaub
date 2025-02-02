from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, CodeDocsSearchTool, ScrapeWebsiteTool
from .tools import open_blender, custom_tool

from crewai.cli.constants import ENV_VARS

# Override the key name dynamically
for entry in ENV_VARS.get("ollama", []):
    if "API_BASE" in entry:
        entry["BASE_URL"] = entry.pop("API_BASE")  # Rename the key

@CrewBase
class Blendercrew():
	"""Blendercrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	
	# -------------------- agent geometry nodes
	@agent
	def agent_geometry_nodes(self) -> Agent:
		return Agent(
			config=self.agents_config['senior_geometry_nodes'],
			verbose=True,
			tools=[custom_tool.MyCustomTool()],
			#memory=True
		)

	@task
	def task_geometry_nodes(self) -> Task:
		return Task(
			config=self.tasks_config['research_geometry_nodes'],
			output_file='agent_geometry_nodes_report.md',
			verbose=True,
			tools=[]
			
		)
	
	# -------------------- agent tutor
	@agent
	def tutor(self) -> Agent:
		return Agent(
			config=self.agents_config['tutor'],
			verbose=True,
			#tools=[open_blender.ScriptTestTool()],
			memory=True
		)

	@task
	def tutoring(self) -> Task:
		return Task(
			config=self.tasks_config['tutoring'],
			output_file='tutorial.md',
			verbose=True,
			tools=[]
			
		)

	manager = Agent(
		role = "Blender programmer Assistant",
		goal = "answer based on blender geometry nodes documentation ",
		backstory = "You're a assistant for blender user , you have to answer question about the blender geometry nodes documentation .",
		allow_delegation=True,
	)
	
	@crew
	def crew(self) -> Crew:
		"""Creates the Blendercrew crew"""

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			#process=Process.sequential,
			verbose=True,
			process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
			manager_agent=self.tutor(),
		)
	
	# @agent
	# def researcher(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['researcher'],
	# 		verbose=True,
	# 		tools=[SerperDevTool()]
	# 	)

	# @agent
	# def reporting_analyst(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['reporting_analyst'],
	# 		verbose=True
	# 	)

	# @agent
	# def translator(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['translator'],
	# 		verbose=True
	# 	)
	# @agent
	# def scrappeur(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['scrappeur'],
	# 		verbose=True,
	# 		tools=[ScrapeWebsiteTool("https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/index.html")]
	# 	)		
	
	# @agent
	# def blender_test(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['blender_test'],
	# 		verbose=True,
	# 		tools=[open_blender.ScriptTestTool()],
	# 		memory=True
	# 	)
	
	# @agent
	# def dev_agent(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['dev_agent'],
	# 		verbose=True,
	# 		tools=[open_blender.ScriptTestTool()],
	# 		memory=True
	# 	)
	

	# @task
	# def research_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['research_task'],
	# 		output_file='english_research.md'
	# 	)
	
	# @task
	# def reporting_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['reporting_task'],
	# 		output_file='english_report.md'
	# 	)
	
	# @task
	# def translating_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['translating_task'],
	# 		output_file='french_report.md'
	# 	)

	# @task
	# def scrapping_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['scrapping_task'],
	# 		output_file='scrapping_report.md',
	# 		verbose=True,
	# 		tools=[ScrapeWebsiteTool()]
			
	# 	)

	# @task
	# def blenderTest_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['blenderTest'],
	# 		output_file='blenderTest_report.md',
	# 		verbose=True,
	# 		tools=[open_blender.ScriptTestTool()]
			
	# 	)
	
	# @task
	# def devAgent_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['devAgent'],
	# 		output_file='devAgent_report.md',
	# 		verbose=True,
	# 		tools=[]
			
	# 	)
	
	