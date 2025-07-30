from adk.type_defs import Message
from adk.agent import Agent
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()  # Loads GEMINI_API_KEY from .env

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class SkillAgent(Agent):
    def __init__(self, config):
        super().__init__(config)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def execute(self, message: Message) -> Message:
        user_input = message.payload.get("text", "")
        prompt = self.build_prompt(user_input)

        response = self.model.generate_content(prompt)
        result = response.text

        return Message(
            payload={"text": result},
            sender=self.name,
            receiver=message.sender
        )

    def build_prompt(self, user_input):
        return f"""
        You are an AI career mentor for a project called SkillBloom.

        User says: "{user_input}"

        Based on this, do the following:
        1. Suggest 3 career paths.
        2. For each path, list the top 3 skills required.
        3. Recommend 1 free online course/resource per path.

        Keep it concise and clean.
        """
