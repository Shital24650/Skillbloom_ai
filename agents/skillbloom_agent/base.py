from adk.type_defs import Message
from adk.agent import Agent
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

class SkillAgent(Agent):
    def __init__(self, config):
        super().__init__(config)
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def execute(self, message: Message) -> Message:
        user_input = message.payload.get("text", "")
        prompt = self.build_prompt(user_input)

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            result = response.text

        except Exception as e:
            result = "⚠️ AI service temporarily unavailable. Please try again."

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
        
