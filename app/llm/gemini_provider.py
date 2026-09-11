"""
Google Gemini LLM Provider implementation using the official google-genai SDK.
"""
from typing import Dict, Any
from app.llm.base import BaseLLMProvider
from app.config import settings
from app.utils.logger import logger

try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class GeminiLLMProvider(BaseLLMProvider):
    def __init__(self, api_key: str = settings.GEMINI_API_KEY, model_name: str = "gemini-2.5-flash"):
        self.api_key = api_key
        self.model_name = model_name
        if not GEMINI_AVAILABLE:
            logger.warning("google-genai SDK not installed. Gemini provider will fall back if invoked.")
            self.client = None
        elif not self.api_key:
            logger.warning("GEMINI_API_KEY not provided. Gemini provider uninitialized.")
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)

    async def generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
        context_details: Dict[str, Any]
    ) -> str:
        if not self.client:
            raise ValueError("Gemini client is not initialized. Please set GEMINI_API_KEY.")

        logger.info(f"LLM PROVIDER | Invoking Gemini model: {self.model_name}")

        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7,
            max_output_tokens=500
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=user_prompt,
            config=config
        )

        return response.text.strip()
