"""
Mock LLM Provider generating realistic, context-grounded astrological responses.
"""
from typing import Dict, Any
from app.llm.base import BaseLLMProvider
from app.utils.logger import logger


class MockLLMProvider(BaseLLMProvider):
    async def generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
        context_details: Dict[str, Any]
    ) -> str:
        """
        Generates an astrological answer grounded in the filtered context details.
        """
        logger.info("LLM PROVIDER | Executing MockLLMProvider generation...")

        user_name = context_details.get("user_name", "there")
        lagna = context_details.get("lagna", "")
        horoscope = context_details.get("horoscope", {})
        houses = context_details.get("houses", {})
        dasha = context_details.get("currentDasha", {})
        panchang = context_details.get("panchang", {})

        # Extract specific insights
        dasha_str = f"{dasha.get('mahadasha', '')}-{dasha.get('antardasha', '')}" if dasha else ""
        house_10_str = f"10th house lord {houses.get('10', {}).get('lord', '')} (Strength: {houses.get('10', {}).get('strength', '')})" if '10' in houses else ""
        house_7_str = f"7th house lord {houses.get('7', {}).get('lord', '')} (Strength: {houses.get('7', {}).get('strength', '')})" if '7' in houses else ""
        house_6_str = f"6th house lord {houses.get('6', {}).get('lord', '')} (Strength: {houses.get('6', {}).get('strength', '')})" if '6' in houses else ""

        career_h = horoscope.get("career", "")
        relationship_h = horoscope.get("relationship", "")
        health_h = horoscope.get("health", "")
        finance_h = horoscope.get("finance", "")

        # Build grounded response based on context present
        answer_parts = []
        answer_parts.append(f"Hello {user_name}!")

        if career_h or house_10_str:
            answer_parts.append(f"Regarding your career transition: Your astrological alignment looks very favorable.")
            if house_10_str:
                answer_parts.append(f"Your {house_10_str} indicates high professional potential and strong recognition.")
            if dasha_str:
                answer_parts.append(f"Under your current {dasha_str} Dasha, key movements and decision points are active.")
            if career_h:
                answer_parts.append(f"Guidance for career: '{career_h}'")

        elif relationship_h or house_7_str:
            answer_parts.append(f"Regarding your relationships:")
            if house_7_str:
                answer_parts.append(f"Your {house_7_str} highlights the importance of patient communication.")
            if relationship_h:
                answer_parts.append(f"Guidance: '{relationship_h}'")

        elif health_h or house_6_str:
            answer_parts.append(f"Regarding health and wellness:")
            if house_6_str:
                answer_parts.append(f"Your {house_6_str} suggests maintaining balance and routine.")
            if health_h:
                answer_parts.append(f"Guidance: '{health_h}'")

        elif finance_h:
            answer_parts.append(f"Regarding financial decisions:")
            if finance_h:
                answer_parts.append(f"Guidance: '{finance_h}'")

        else:
            answer_parts.append("Based on your planetary configuration, today is an opportune day for strategic planning and steady progress.")

        if panchang.get("tithi"):
            answer_parts.append(f"Today's Panchang ({panchang.get('tithi')}, {panchang.get('nakshatra')} Nakshatra) supports clear decision-making.")

        answer_parts.append("Trust your intuition and take calculated steps towards your goal!")

        return " ".join(answer_parts)
