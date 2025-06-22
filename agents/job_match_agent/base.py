# agents/job_match_agent/base.py

from adk.type_defs import Message
from adk.agent import Agent
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class JobMatchAI(Agent):
    def __init__(self, config=None):
        super().__init__(config)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def execute(self, message: Message) -> Message:
        user_input = message.payload.get("text", "")
        response = self.model.generate_content(user_input)
        return Message(
            payload={"text": response.text},
            sender=self.name,
            receiver=message.sender
        )
