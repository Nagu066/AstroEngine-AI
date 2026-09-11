"""
OpenAI LLM Provider implementation.
"""
from typing import Dict, Any
from app.llm.base import BaseLLMProvider
from app.config import settings
from app.utils.logger import logger

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class OpenAILLMProvider(BaseLLMProvider):
    def __init__(self, api_key: str = settings.OPENAI_API_KEY, model_name: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model_name = model_name
        if not OPENAI_AVAILABLE or not self.api_key:
            self.client = None
        else:
            self.client = openai.AsyncOpenAI(api_key=self.api_key)

    async def generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
        context_details: Dict[str, Any]
    ) -> str:
        if not self.client:
            raise ValueError("OpenAI client is not initialized. Please set OPENAI_API_KEY.")

        logger.info(f"LLM PROVIDER | Invoking OpenAI model: {self.model_name}")

        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content.strip()
