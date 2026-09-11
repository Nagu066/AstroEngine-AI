"""
Unit tests for Personalization Context Selection and Filtering.
"""
import pytest
from app.engine.context_selector import context_selector
from app.models.domain import IntentResult


def test_context_selection_for_career_intent():
    intent = IntentResult(intent="career", confidence_score=0.9, detected_keywords=["job"])
    raw_context = {
        "user": {"name": "Aarav", "language": "en", "subscription": "premium", "tonePreference": "motivational"},
        "kundli": {
            "lagna": "Libra",
            "moonSign": "Scorpio",
            "currentDasha": {"mahadasha": "Rahu", "antardasha": "Mars"},
            "houses": {
                "6": {"lord": "Jupiter", "strength": "Average"},
                "7": {"lord": "Mars", "strength": "Weak"},
                "10": {"lord": "Moon", "strength": "Strong"}
            }
        },
        "horoscope": {
            "career": "Networking may bring new opportunities.",
            "relationship": "Communication improves.",
            "health": "Prioritize proper sleep."
        },
        "panchang": {"tithi": "Shukla Panchami"}
    }

    config, filtered = context_selector.select_context(intent, raw_context)

    # 1. Career Horoscope and 10th House must be selected
    assert "Career Horoscope" in config.selectedContext
    assert "10th House" in config.selectedContext
    
    # 2. Relationship Horoscope must be EXCLUDED
    assert "Relationship Horoscope" in config.excludedContext
    assert "relationship" not in filtered["horoscope"]
    assert "7" not in filtered["houses"]


def test_context_selection_for_relationship_intent():
    intent = IntentResult(intent="relationship", confidence_score=0.9, detected_keywords=["love"])
    raw_context = {
        "user": {"name": "Priya", "language": "hi", "subscription": "free", "tonePreference": "compassionate"},
        "kundli": {
            "lagna": "Cancer",
            "currentDasha": {"mahadasha": "Jupiter", "antardasha": "Venus"},
            "houses": {"7": {"lord": "Saturn", "strength": "Strong"}}
        },
        "horoscope": {
            "career": "Patience at work.",
            "relationship": "Harmonious time."
        }
    }

    config, filtered = context_selector.select_context(intent, raw_context)

    assert "Relationship Horoscope" in config.selectedContext
    assert "7th House" in config.selectedContext
    assert "Career Horoscope" in config.excludedContext
    assert "career" not in filtered["horoscope"]
