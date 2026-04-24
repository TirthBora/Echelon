import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ai.ai_engine import ask_ai

def test_ai():
    response = ask_ai("What is ModuleNotFoundErrors?")
    

    assert ininstance(response,str)
    assert len(response.strip())>0

