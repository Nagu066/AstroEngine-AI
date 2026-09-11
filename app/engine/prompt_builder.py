"""
Prompt Construction Engine for building optimized System and User prompts for LLMs.
"""
import json
from typing import Dict, Any, Tuple
from app.models.domain import PersonalizationConfig
from app.utils.metrics import calculate_prompt_metrics
from app.utils.logger import logger


class PromptBuilder:
    def build_prompts(
        self,
        question: str,
        config: PersonalizationConfig,
        filtered_context: Dict[str, Any]
    ) -> Tuple[str, str, Dict[str, Any]]:
        """
        Constructs personalized System Prompt and User Prompt using ONLY selected context.
        Returns:
            - system_prompt (str)
            - user_prompt (str)
            - prompt_metrics (Dict[str, Any])
        """
        language = config.language
        tone = config.tone
        max_words = config.maxWords
        intent = config.intent

        # Construct System Prompt
        system_prompt = (
            f"You are MyNaksh's expert AI Vedic Astrologer.\n"
            f"Your mission is to provide deeply personalized, compassionate, and actionable astrological guidance.\n\n"
            f"CRITICAL GUIDELINES:\n"
            f"1. LANGUAGE: Respond strictly in {language}.\n"
            f"2. TONE: Maintain a {tone} tone throughout your response.\n"
            f"3. LENGTH: Keep your answer under approximately {max_words} words.\n"
            f"4. GROUNDING: Rely ONLY on the astrological context provided in the user message. "
            f"Do NOT invent unmentioned planetary placements or transits.\n"
            f"5. CLARITY: Focus directly on the user's {intent.upper()} query."
        )

        # Construct User Prompt with formatted selected context
        formatted_context_str = json.dumps(filtered_context, indent=2, ensure_ascii=False)
        
        user_prompt = (
            f"USER QUESTION:\n\"{question}\"\n\n"
            f"PERSONALIZED ASTROLOGICAL CONTEXT (SELECTED FOR {intent.upper()} INTENT):\n"
            f"```json\n{formatted_context_str}\n```\n\n"
            f"SOURCES USED: {', '.join(config.selectedContext)}\n\n"
            f"Please synthesize this specific astrological context to directly answer the user's question. "
            f"Be encouraging, concise, and well-structured."
        )

        # Calculate character and token metrics
        metrics = calculate_prompt_metrics(system_prompt, user_prompt)

        return system_prompt, user_prompt, metrics


# Global instance
prompt_builder = PromptBuilder()
