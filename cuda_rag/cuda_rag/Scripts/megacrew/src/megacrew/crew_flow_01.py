# importation par default 
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.flow.flow import Flow, listen, start

from pydantic import BaseModel
from typing import List


# Autre importation 
from src.megacrew.tools.custom_tool  import  MyCustomTool
from crewai.cli.constants import ENV_VARS
# Override the key name dynamically
for entry in ENV_VARS.get("ollama", []):
    if "API_BASE" in entry:
        entry["BASE_URL"] = entry.pop("API_BASE")  # Rename the key


class BlogState(BaseModel):
    topic: str = "creating a modifier made with geometry node editor, that allows to modify the level of subdivision of an object, according to the distance to the camera."
    research_notes: List[str] = []
    draft_content: str = ""
    final_content: str = ""
    translate_content: str = ""


class Megacrew(Flow[BlogState]):
    def __init__(self):
        super().__init__()
        # Initialize agents for different crews
        self.researcher = Agent(
            role="Senior Data Researcher",
      		goal="answer tutor question based on blender geometry nodes documentation",
       		backstory="""You're working with blender user , you have to answer question using the documentation of blender geometry nodes.
            You are known for your ability to find the most relevant information and present it in a clear and concise manner.""",
			tools=[MyCustomTool()],
      
        )
        self.writer = Agent(
            role="blender teacher",
			goal=f"create detailed tutorial about {self.state.topic}.",
			backstory="""You're a meticulous analyst with a keen eye for detail. You're known for
			your ability to turn complex data into clear and concise reports, making
			it easy for others to understand and act on the information you provide.""",
		)
        self.translator = Agent(
            role ="translator english to french",
  			goal=f"you have to translate the {self.state.final_content} to french.",
  			backstory="""You're a meticulous translator english to french. you have ability in translation for technical documentation.
    		you''ll keep technical terms in english and translate the rest to french."""
		)
    
  
        
                

    @start()
    def generate_topic(self):
        # Create a research crew
        research_crew = Crew(
            agents=[self.writer],
            tasks=[
                Task(
                    description=f"you should produce a clear and concise tutorial for blender geometry nodes.the subject of this tutorial is {self.state.topic}.",
                    agent=self.writer,
                    expected_output=f"a clear draft explaining how to build the geometry node group responding to {self.state.topic}"
                )
            ]
        )      
        draft = research_crew.kickoff()
        print("draft = ",draft)
        self.state.draft_content = draft
        return draft
    
    @listen(generate_topic)
    def list_points(self, draft):
        # Create a list of technical point to have a look
        research_crew = Crew(
            agents=[self.writer],
            tasks=[
                Task(
                    description=f"create a list of nodes needed for {draft}",
                    agent=self.researcher,
                    expected_output="a list of technical nodes listed by name."
                ),                
            ]
        )
        
        research_results = research_crew.kickoff()
        themes = []
        
        for p in str(research_results).split("\n"):
             themes.append(p)
        print("research_results = ",themes)
        self.state.research_notes = research_results #research_results       
        return themes#research_results

    @listen(list_points)
    def conduct_research(self, topic):
        # Create a research crew with specific research tasks
        conduct_crew = Crew(
            agents=[self.researcher],
            tasks=[
                Task(
                    description=f"Research info about each points of the list: {self.state.research_notes}",
                    agent=self.researcher,
                    tools=[MyCustomTool()],
                    expected_output=f"a list of resume of what you find for each item in the {self.state.research_notes}."
                )
            ]
        )
        
        conduct_results = conduct_crew.kickoff()
        print("conduct_results = ",conduct_results)
        self.state.research_notes = conduct_results
        return conduct_results

    @listen(conduct_research)
    def edit_content(self):
        # Create an editing crew       
        editing_crew = Crew(
            agents=[self.writer],
            tasks=[
                Task(
                    description=f"Edit and improve this tutorial: {self.state.draft_content}, with this infos: {self.state.research_notes}",
                    agent=self.writer,
                    expected_output="a final tutorial.",
                    output_file='english_tutorial.md'
                )
            ]
        )
        
        final_content = editing_crew.kickoff()
        print("final_content = ",final_content)
        self.state.final_content = final_content
        return final_content
    
    @listen(edit_content)
    def translate_content(self):
        # Translating crew       
        translate_crew = Crew(
            agents=[self.translator],
            tasks=[
                Task(
                    description=f"translate from english to french {self.state.final_content}",
                    agent=self.translator,
                    expected_output="a french translation of the tutorial.",
                    output_file='french_tutorial.md'
                )
            ]
        )
        
        translate_content = translate_crew.kickoff()
        print("french_content = ",translate_content)
        self.state.translate_content = translate_content
        return translate_content

    

