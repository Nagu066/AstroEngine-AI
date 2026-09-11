"""
Application configuration settings for AstroEngine AI Personalization & Context Engine.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    PROJECT_NAME: str = "AstroEngine AI - Personalization & Context Orchestrator"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("true", "1")

    # Server configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Upstream Services URLs
    USER_SERVICE_URL: str = os.getenv("USER_SERVICE_URL", "http://localhost:8000/users")
    KUNDLI_SERVICE_URL: str = os.getenv("KUNDLI_SERVICE_URL", "http://localhost:8000/kundli")
    HOROSCOPE_SERVICE_URL: str = os.getenv("HOROSCOPE_SERVICE_URL", "http://localhost:8000/horoscope")
    PANCHANG_SERVICE_URL: str = os.getenv("PANCHANG_SERVICE_URL", "http://localhost:8000/panchang")

    # Upstream Resiliency Settings
    UPSTREAM_TIMEOUT_SECONDS: float = float(os.getenv("UPSTREAM_TIMEOUT_SECONDS", "2.0"))
    UPSTREAM_MAX_RETRIES: int = int(os.getenv("UPSTREAM_MAX_RETRIES", "2"))
    UPSTREAM_CACHE_TTL_SECONDS: int = int(os.getenv("UPSTREAM_CACHE_TTL_SECONDS", "300"))

    # LLM Settings
    # Supported providers: 'mock', 'gemini', 'openai'
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "mock").lower()
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-2.5-flash" if os.getenv("GEMINI_API_KEY") else "gpt-4o-mini")

    # Path to personalization rules JSON
    RULES_FILE_PATH: Path = BASE_DIR / "app" / "rules" / "personalization_rules.json"

settings = Settings()
