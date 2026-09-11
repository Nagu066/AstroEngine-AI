"""
Intent Detection Engine for categorizing user astrological questions.
"""
import re
from typing import Dict, List, Tuple
from app.models.domain import IntentResult
from app.utils.logger import logger


INTENT_PATTERNS: Dict[str, List[str]] = {
    "career": [
        r"\bjob\b", r"\bcareer\b", r"\bwork\b", r"\bprofession\b", r"\bpromotion\b",
        r"\bsalary\b", r"\binterview\b", r"\bbusiness\b", r"\bcompany\b", r"\boffer\b",
        r"\bposition\b", r"\bswitch\b", r"\bchanging my job\b", r"\bnew job\b"
    ],
    "relationship": [
        r"\brelationship\b", r"\blove\b", r"\bpartner\b", r"\bmarriage\b", r"\bmarry\b",
        r"\bdating\b", r"\bspouse\b", r"\bboyfriend\b", r"\bgirlfriend\b", r"\bhusband\b",
        r"\bwife\b", r"\bdivorce\b", r"\bfamily\b", r"\bcompatibility\b"
    ],
    "health": [
        r"\bhealth\b", r"\bwellness\b", r"\bsickness\b", r"\bmedical\b", r"\bdiet\b",
        r"\bsleep\b", r"\bexercise\b", r"\bstress\b", r"\bmental\b", r"\benergy\b",
        r"\bfitness\b", r"\body\b", r"\bhealing\b"
    ],
    "finance": [
        r"\bfinance\b", r"\bmoney\b", r"\binvest\b", r"\binvestment\b", r"\bstocks\b",
        r"\bproperty\b", r"\bwealth\b", r"\bdebt\b", r"\bloan\b", r"\bexpense\b",
        r"\bcrypto\b", r"\bfinancial\b", r"\bprofit\b"
    ]
}


class IntentDetector:
    def detect_intent(self, question: str) -> IntentResult:
        """
        Analyzes question text to classify intent into career, relationship, health, finance, or general.
        """
        question_clean = question.lower().strip()
        matched_scores: Dict[str, Tuple[int, List[str]]] = {}

        for intent, patterns in INTENT_PATTERNS.items():
            matches = []
            for pattern in patterns:
                if re.search(pattern, question_clean):
                    matches.append(pattern.replace(r"\b", "").strip())
            if matches:
                matched_scores[intent] = (len(matches), matches)

        if matched_scores:
            # Pick intent with highest match count
            top_intent = max(matched_scores.keys(), key=lambda k: matched_scores[k][0])
            match_count, keywords = matched_scores[top_intent]
            confidence = min(0.95, 0.70 + (match_count * 0.10))
            logger.info(f"INTENT DETECTED | Intent: {top_intent} | Confidence: {confidence} | Keywords: {keywords}")
            return IntentResult(
                intent=top_intent,
                confidence_score=confidence,
                detected_keywords=keywords
            )

        # Default fallback to general intent
        logger.info(f"INTENT DETECTED | Fallback to 'general' for question: '{question}'")
        return IntentResult(
            intent="general",
            confidence_score=0.60,
            detected_keywords=["general_question"]
        )


# Global instance
intent_detector = IntentDetector()
