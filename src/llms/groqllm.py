import os
from groq import Groq
from src.utils.config import GROQ_API_KEY, GROQ_MODEL
from src.utils.logging import get_logger

logger = get_logger("GroqLLM")

class GroqLLM:
    def __init__(self, model: str = GROQ_MODEL):
        if not GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY missing in .env")
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = model
        logger.info(f"Using Groq model: {self.model}")

    def chat(self, prompt: str) -> str:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=800,
        )
        return resp.choices[0].message.content
