from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, CodeDocsSearchTool, ScrapeWebsiteTool
from Scripts.blendercrew.src.blendercrew.tools import open_blender, custom_tool
from crewai import LLM
from dotenv import load_dotenv
load_dotenv()


from crewai.cli.constants import ENV_VARS

# Override the key name dynamically
for entry in ENV_VARS.get("ollama", []):
    if "API_BASE" in entry:
        entry["BASE_URL"] = entry.pop("API_BASE")  # Rename the key

llm = LLM(
    model="ollama/mixtral"
)


# Define the  agents: 

manager = Agent(
	role="Project Manager",
	goal="Efficiently manage the crew and ensure high-quality task completion",
	backstory="You're an experienced project manager, skilled in overseeing complex projects and guiding teams to success. Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time and to the highest standard.",
	allow_delegation=True,
)

researcher = Agent(
	role="Senior data resercher",
	goal="answer based on blender geometry nodes documentation.",
	backstory="""You're working with blender user , you have to answer question using the documentation of blender geometry nodes.
		You are known for your ability to find the most relevant information and present it in a clear and concise manner.""",
	allow_delegation=False,
    tools=[custom_tool.MyCustomTool()]
)


task = Task(
	description="In this task you should produce a a clear and concise tutorial for blender geometry nodes.\
		the subject of this tutorial is {goal}. start by making a plan of the geometry nodes group you have to build to achieve the goal of the tutorial:{goal}.\
		for each node, you could ask to agent resercher any details you need from documentation.\
		make sure that every node or node property you want to use exists.\
		if not, imagine what kind of node could exist that would allow you to do so.\
		in each case, you can ask the resercher agent for detailed information about blender's geometry node system.\
		do not makeup imaginary tools on your own.\
		task output is a string.",
    expected_output="a clear and concise tutorial explaining how to build the geometry node group responding to {goal}",
    agent = manager
	)



# Instantiate your crew with a custom manager
crew = Crew(           
	agents=[researcher],
	tasks=[task],
    manager_llm=llm,
	manager_agent=manager,
	process=Process.hierarchical,
    model = llm#"ollama/mixtral"
)

result = crew.kickoff()


# @CrewBase
# class Blendercrew():
	# """Blendercrew crew"""

	# agents_config = 'config/agents.yaml'
	# tasks_config = 'config/tasks.yaml'
	
	# # -------------------- agent geometry nodes
	# @agent
	# def agent_geometry_nodes(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['senior_geometry_nodes'],
	# 		verbose=True,
	# 		tools=[custom_tool.MyCustomTool()],
	# 		#memory=True
	# 	)

	# @task
	# def task_geometry_nodes(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['research_geometry_nodes'],
	# 		output_file='agent_geometry_nodes_report.md',
	# 		verbose=True,
	# 		tools=[]
			
	# 	)
	
	# # -------------------- agent tutor
	# @agent
	# def tutor(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['tutor'],
	# 		verbose=True,
	# 		#tools=[open_blender.ScriptTestTool()],
	# 		memory=True
	# 	)

	# @task
	# def tutoring(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['tutoring'],
	# 		output_file='tutorial.md',
	# 		verbose=True,
	# 		tools=[]
			
	# 	)

	
	# @crew
	# def crew(self) -> Crew:
	# 	"""Creates the Blendercrew crew"""

	# 	return Crew(
	# 		agents=self.agents, # Automatically created by the @agent decorator
	# 		tasks=self.tasks, # Automatically created by the @task decorator
	# 		#process=Process.sequential,
	# 		verbose=True,
	# 		process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
	# 		manager_agent=self.tutor(),
	# 	)
	


	# Define your agents
	
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
	
	