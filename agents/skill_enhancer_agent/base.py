# agents/skill_enhancer_agent/base.py

from adk.type_defs import Message
from adk.agent import Agent
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"

class SkillEnhancerAI(Agent):
    def __init__(self, config=None):
        super().__init__(config)
        self.model = "llama3-8b-8192"  # or "mixtral-8x7b-32768"

    def execute(self, message: Message) -> Message:
        user_input = message.payload.get("text", "")

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a skill enhancement assistant. Given a user's input, provide personalized guidance "
                        "on how they can improve their technical and soft skills, including tools, courses, or projects."
                    )
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            temperature=0.7
        )

        reply = response["choices"][0]["message"]["content"]

        return Message(
            payload={"text": reply},
            sender=self.name,
            receiver=message.sender
        )
