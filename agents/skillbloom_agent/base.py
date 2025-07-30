# agents/skillbloom_agent/base.py

from adk.type_defs import Message
from adk.agent import Agent
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Loads GROQ_API_KEY from .env

openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"

class SkillAgent(Agent):
    def __init__(self, config):
        super().__init__(config)
        self.model = "llama3-8b-8192"  # or "mixtral-8x7b-32768"

    def execute(self, message: Message) -> Message:
        user_input = message.payload.get("text", "")
        prompt = self.build_prompt(user_input)

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI career mentor for a project called SkillBloom. "
                        "Provide practical, concise, and personalized career guidance."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )

        result = response["choices"][0]["message"]["content"]

        return Message(
            payload={"text": result},
            sender=self.name,
            receiver=message.sender
        )

    def build_prompt(self, user_input):
        return f"""
User says: "{user_input}"

Based on this, do the following:
1. Suggest 3 career paths.
2. For each path, list the top 3 skills required.
3. Recommend 1 free online course/resource per path.

Keep it concise and clean.
"""
