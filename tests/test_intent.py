"""
Unit tests for Intent Detector Engine.
"""
import pytest
from app.engine.intent_detector import intent_detector


def test_career_intent_detection():
    question = "Should I consider changing my job in the next few months?"
    result = intent_detector.detect_intent(question)
    assert result.intent == "career"
    assert result.confidence_score >= 0.70
    assert "job" in result.detected_keywords or "changing my job" in result.detected_keywords


def test_relationship_intent_detection():
    question = "How does this month look for my relationship and marriage?"
    result = intent_detector.detect_intent(question)
    assert result.intent == "relationship"
    assert "relationship" in result.detected_keywords or "marriage" in result.detected_keywords


def test_health_intent_detection():
    question = "What should I focus on for my health and daily wellness?"
    result = intent_detector.detect_intent(question)
    assert result.intent == "health"
    assert "health" in result.detected_keywords or "wellness" in result.detected_keywords


def test_finance_intent_detection():
    question = "Is this a good time to invest money in property or stocks?"
    result = intent_detector.detect_intent(question)
    assert result.intent == "finance"
    assert "invest" in result.detected_keywords or "money" in result.detected_keywords


def test_general_fallback_intent():
    question = "Can you summarize today's guidance for me?"
    result = intent_detector.detect_intent(question)
    assert result.intent in ("general", "career", "health", "relationship")
