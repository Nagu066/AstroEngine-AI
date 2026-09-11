"""
Configuration-Driven Context Selector.
Filters raw upstream microservice data according to rule configurations.
"""
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple
from app.config import settings
from app.models.domain import PersonalizationConfig, IntentResult
from app.utils.logger import logger


class ContextSelector:
    def __init__(self, rules_path: Path = settings.RULES_FILE_PATH):
        self.rules_path = rules_path
        self.rules = self._load_rules()

    def _load_rules(self) -> Dict[str, Any]:
        try:
            with open(self.rules_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.error(f"Failed to load personalization rules from {self.rules_path}: {exc}")
            # Fallback basic rule mapping
            return {
                "intents": {
                    "general": {
                        "primary_sources": ["Career Horoscope", "Relationship Horoscope", "Health Horoscope", "10th House", "7th House", "6th House"],
                        "secondary_sources": ["Current Dasha", "Panchang"],
                        "exclude_sources": [],
                        "houses_to_include": ["6", "7", "10"],
                        "include_dasha": True,
                        "include_panchang": True,
                        "horoscope_keys": ["career", "finance", "health", "relationship"]
                    }
                },
                "subscription_tier_words": {"free": 150, "standard": 200, "premium": 250},
                "language_names": {"en": "English", "hi": "Hindi", "es": "Spanish"}
            }

    def select_context(
        self,
        intent_result: IntentResult,
        raw_context: Dict[str, Any]
    ) -> Tuple[PersonalizationConfig, Dict[str, Any]]:
        """
        Filters raw upstream context based on configuration rules for the detected intent.
        Returns:
            - PersonalizationConfig metadata (intent, language, tone, maxWords, selectedContext, excludedContext)
            - Filtered context dictionary ready for prompt construction.
        """
        intent_name = intent_result.intent
        intent_rules = self.rules.get("intents", {}).get(intent_name) or self.rules.get("intents", {}).get("general")

        user_data = raw_context.get("user") or {}
        kundli_data = raw_context.get("kundli") or {}
        horoscope_data = raw_context.get("horoscope") or {}
        panchang_data = raw_context.get("panchang") or {}

        # Resolve Language & Tone
        lang_code = user_data.get("language", "en")
        language_name = self.rules.get("language_names", {}).get(lang_code, "English")
        
        tone_pref = user_data.get("tonePreference", "motivational").capitalize()
        
        subscription = user_data.get("subscription", "free").lower()
        max_words = self.rules.get("subscription_tier_words", {}).get(subscription, 200)

        # Selected and Excluded Sources
        selected_sources: List[str] = []
        excluded_sources: List[str] = intent_rules.get("exclude_sources", [])

        filtered_context: Dict[str, Any] = {
            "user_name": user_data.get("name", "User"),
            "lagna": kundli_data.get("lagna"),
            "moonSign": kundli_data.get("moonSign")
        }

        # 1. Horoscope Filtering
        allowed_horoscope_keys = intent_rules.get("horoscope_keys", [])
        filtered_horoscope = {}
        for key in allowed_horoscope_keys:
            if key in horoscope_data and horoscope_data[key]:
                filtered_horoscope[key] = horoscope_data[key]
                source_name = f"{key.capitalize()} Horoscope"
                if source_name not in selected_sources:
                    selected_sources.append(source_name)

        filtered_context["horoscope"] = filtered_horoscope

        # 2. Kundli House Filtering
        houses_to_include = intent_rules.get("houses_to_include", [])
        raw_houses = kundli_data.get("houses", {})
        filtered_houses = {}
        for house_num in houses_to_include:
            if house_num in raw_houses:
                filtered_houses[house_num] = raw_houses[house_num]
                house_source = f"{house_num}th House"
                if house_source not in selected_sources:
                    selected_sources.append(house_source)

        filtered_context["houses"] = filtered_houses

        # 3. Dasha Filtering
        if intent_rules.get("include_dasha", True) and "currentDasha" in kundli_data:
            filtered_context["currentDasha"] = kundli_data["currentDasha"]
            if "Current Dasha" not in selected_sources:
                selected_sources.append("Current Dasha")

        # 4. Panchang Filtering
        if intent_rules.get("include_panchang", True) and panchang_data:
            filtered_context["panchang"] = panchang_data
            if "Today's Panchang" not in selected_sources and "Panchang" not in selected_sources:
                selected_sources.append("Current Panchang" if "Panchang" in intent_rules.get("secondary_sources", []) else "Today's Panchang")

        # Ensure Moon Sign source tracking if relevant
        if "Moon Sign" in intent_rules.get("secondary_sources", []) and kundli_data.get("moonSign"):
            if "Moon Sign" not in selected_sources:
                selected_sources.append("Moon Sign")

        config = PersonalizationConfig(
            intent=intent_name,
            language=language_name,
            tone=tone_pref,
            maxWords=max_words,
            selectedContext=selected_sources,
            excludedContext=excluded_sources,
            context_details=filtered_context
        )

        logger.info(
            f"CONTEXT FILTERED | Intent: {intent_name} | Selected ({len(selected_sources)}): {selected_sources} | "
            f"Excluded ({len(excluded_sources)}): {excluded_sources}"
        )

        return config, filtered_context


# Global instance
context_selector = ContextSelector()
