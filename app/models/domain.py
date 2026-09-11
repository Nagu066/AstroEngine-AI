"""
Domain data models for User, Kundli, Horoscope, Panchang, and Personalization entities.
"""
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class BirthDetails(BaseModel):
    date: str
    time: str
    place: str


class UserProfile(BaseModel):
    id: str
    name: str
    language: str = "en"
    subscription: str = "free"
    tonePreference: str = "motivational"
    birthDetails: Optional[BirthDetails] = None


class HouseDetail(BaseModel):
    lord: str
    strength: str


class DashaInfo(BaseModel):
    mahadasha: str
    antardasha: str


class KundliData(BaseModel):
    lagna: str
    moonSign: str
    currentDasha: DashaInfo
    houses: Dict[str, HouseDetail] = Field(default_factory=dict)


class HoroscopeData(BaseModel):
    career: Optional[str] = None
    finance: Optional[str] = None
    health: Optional[str] = None
    relationship: Optional[str] = None


class PanchangData(BaseModel):
    date: str
    tithi: str
    nakshatra: str
    yoga: str
    karana: str


class IntentResult(BaseModel):
    intent: str
    confidence_score: float
    detected_keywords: List[str] = Field(default_factory=list)


class PersonalizationConfig(BaseModel):
    intent: str
    language: str
    tone: str
    maxWords: int
    selectedContext: List[str]
    excludedContext: List[str]
    context_details: Dict[str, Any] = Field(default_factory=dict)
