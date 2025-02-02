#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from megacrew.crew import Megacrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'blender_manual': 'https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/index.html',
        'source':'geometry_node_editor_guide.pdf',
        'topic': ' geometry node editor',
        'current_version': '4.0',
        'goal':'creating a modifier made with geometry node editor, that allows to modify the level of subdivision of an object, according to the distance to the camera.',
        'script':'C:/Users/isisc/IA/cuda_rag/cuda_rag/Scripts/blendercrew/src/blendercrew/tools/testScript.py'
    }
    try:
        Megacrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Megacrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Megacrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Megacrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
