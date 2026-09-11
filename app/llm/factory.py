"""
Factory to instantiate LLM Providers based on settings and environment.
"""
from app.config import settings
from app.llm.base import BaseLLMProvider
from app.llm.mock_provider import MockLLMProvider
from app.llm.gemini_provider import GeminiLLMProvider
from app.llm.openai_provider import OpenAILLMProvider
from app.utils.logger import logger


def get_llm_provider(provider_type: str = settings.LLM_PROVIDER) -> BaseLLMProvider:
    provider = provider_type.lower()
    
    if provider == "gemini" and settings.GEMINI_API_KEY:
        try:
            return GeminiLLMProvider()
        except Exception as exc:
            logger.warning(f"Failed to instantiate GeminiLLMProvider ({exc}). Falling back to MockLLMProvider.")
            return MockLLMProvider()
            
    if provider == "openai" and settings.OPENAI_API_KEY:
        try:
            return OpenAILLMProvider()
        except Exception as exc:
            logger.warning(f"Failed to instantiate OpenAILLMProvider ({exc}). Falling back to MockLLMProvider.")
            return MockLLMProvider()

    # Default to Mock LLM Provider
    logger.info("Using default MockLLMProvider.")
    return MockLLMProvider()
