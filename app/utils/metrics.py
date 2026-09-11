"""
Prompt metrics calculation and token estimation utilities.
"""
from typing import Tuple, Dict, Any
from app.utils.logger import logger


def calculate_prompt_metrics(system_prompt: str, user_prompt: str) -> Dict[str, Any]:
    """
    Calculates character count and estimated token count for system and user prompts.
    Standard heuristic: ~4 characters per token for English/astrological text.
    """
    total_text = f"{system_prompt}\n{user_prompt}"
    char_count = len(total_text)
    # 1 token is roughly 4 characters in English
    estimated_tokens = max(1, round(char_count / 4.0))

    metrics = {
        "character_count": char_count,
        "estimated_token_count": estimated_tokens,
        "system_prompt_length": len(system_prompt),
        "user_prompt_length": len(user_prompt),
        "system_prompt_snippet": system_prompt[:120] + "..." if len(system_prompt) > 120 else system_prompt,
        "user_prompt_snippet": user_prompt[:120] + "..." if len(user_prompt) > 120 else user_prompt,
    }

    logger.info(
        f"PROMPT METRICS | Total Chars: {char_count} | Est Tokens: {estimated_tokens} | "
        f"Sys Chars: {len(system_prompt)} | User Chars: {len(user_prompt)}"
    )

    return metrics
