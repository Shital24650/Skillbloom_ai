import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from agents.skillbloom_agent.base import SkillAgent
from adk.type_defs import Message

agent = SkillAgent(config={})

user_input = input("Enter your interest or skill to explore: ")
message = Message(payload={"text": user_input}, sender="user", receiver="SkillAgent")
response = agent.execute(message)

print("\n=== SkillBloom AI Suggestions ===\n")
print(response.payload["text"])