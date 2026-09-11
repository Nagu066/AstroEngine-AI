"""
Base LLM Provider Abstract Interface.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
        context_details: Dict[str, Any]
    ) -> str:
        """
        Generates a text completion based on system prompt and user prompt.
        """
        pass
