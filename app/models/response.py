"""
API Response payload schemas.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class PersonalizeResponse(BaseModel):
    answer: str = Field(..., description="Grounded personalized AI generated response")
    confidence: str = Field(..., description="Confidence level of the response: HIGH, MEDIUM, LOW")
    sourcesUsed: List[str] = Field(..., description="List of astrological sources utilized for generating answer")


class PromptMetrics(BaseModel):
    character_count: int
    estimated_token_count: int
    system_prompt_snippet: str
    user_prompt_snippet: str


class DebugResponse(BaseModel):
    intent: str = Field(..., description="Detected user query intent")
    selectedContext: List[str] = Field(..., description="Context items selected for LLM prompt")
    excludedContext: List[str] = Field(..., description="Context items explicitly excluded from LLM prompt")
    language: str = Field(..., description="Configured response language")
    tone: str = Field(..., description="Configured response tone")
    maxWords: Optional[int] = Field(None, description="Configured max words limit based on user tier")
    promptMetrics: Optional[PromptMetrics] = Field(None, description="Prompt size and token metrics")
    upstreamStatus: Optional[Dict[str, str]] = Field(None, description="Status of upstream microservice calls")
