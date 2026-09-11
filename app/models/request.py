"""
API Request payload schemas.
"""
from pydantic import BaseModel, Field


class PersonalizeRequest(BaseModel):
    userId: str = Field(..., description="Unique ID of the user requesting context", json_schema_extra={"example": "user_101"})
    question: str = Field(..., description="User's astrological or life question", json_schema_extra={"example": "Should I consider changing my job in the next few months?"})


class DebugRequest(BaseModel):
    userId: str = Field(..., description="Unique ID of the user requesting debug personalization", json_schema_extra={"example": "user_101"})
    question: str = Field(..., description="User's astrological or life question", json_schema_extra={"example": "Should I consider changing my job in the next few months?"})
