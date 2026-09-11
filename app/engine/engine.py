"""
Personalization Engine Orchestrator.
Main entry point coordinating Intent Detection, Context Selection, Prompt Construction, and LLM Completion.
"""
from typing import Dict, Any, Tuple
from app.upstream.client import UpstreamClientManager
from app.engine.intent_detector import intent_detector, IntentDetector
from app.engine.context_selector import context_selector, ContextSelector
from app.engine.prompt_builder import prompt_builder, PromptBuilder
from app.llm.factory import get_llm_provider
from app.llm.base import BaseLLMProvider
from app.models.domain import PersonalizationConfig, IntentResult
from app.models.response import PersonalizeResponse, DebugResponse, PromptMetrics
from app.utils.logger import logger, log_latency


class PersonalizationEngine:
    def __init__(
        self,
        upstream_manager: UpstreamClientManager = UpstreamClientManager(),
        detector: IntentDetector = intent_detector,
        selector: ContextSelector = context_selector,
        builder: PromptBuilder = prompt_builder,
        llm_provider: BaseLLMProvider = get_llm_provider()
    ):
        self.upstream_manager = upstream_manager
        self.intent_detector = detector
        self.context_selector = selector
        self.prompt_builder = builder
        self.llm_provider = llm_provider

    async def get_debug_personalization(self, user_id: str, question: str) -> DebugResponse:
        """
        Executes Intent Detection, Upstream Fetching, and Context Selection WITHOUT invoking LLM.
        Returns detailed debug output.
        """
        with log_latency(f"Debug Personalization Pipeline user={user_id}"):
            # 1. Fetch Upstream Data
            raw_context, upstream_statuses = await self.upstream_manager.fetch_all_context(user_id)

            # 2. Detect Intent
            intent_result = self.intent_detector.detect_intent(question)

            # 3. Filter Context via Rules
            config, filtered_context = self.context_selector.select_context(intent_result, raw_context)

            # 4. Build Prompts for Metrics
            system_prompt, user_prompt, metrics = self.prompt_builder.build_prompts(
                question, config, filtered_context
            )

        return DebugResponse(
            intent=config.intent,
            selectedContext=config.selectedContext,
            excludedContext=config.excludedContext,
            language=config.language,
            tone=config.tone,
            maxWords=config.maxWords,
            promptMetrics=PromptMetrics(**metrics),
            upstreamStatus=upstream_statuses
        )

    async def personalize_response(self, user_id: str, question: str) -> PersonalizeResponse:
        """
        Executes complete pipeline: Upstream Fetch -> Intent -> Context Selection -> Prompt -> LLM -> Response.
        """
        with log_latency(f"Full Personalize Pipeline user={user_id}"):
            # 1. Fetch Upstream Data Concurrently
            raw_context, upstream_statuses = await self.upstream_manager.fetch_all_context(user_id)

            # 2. Intent Classification
            intent_result = self.intent_detector.detect_intent(question)

            # 3. Context Selection & Filtering
            config, filtered_context = self.context_selector.select_context(intent_result, raw_context)

            # 4. Construct System & User Prompts
            system_prompt, user_prompt, metrics = self.prompt_builder.build_prompts(
                question, config, filtered_context
            )

            # 5. Invoke LLM Provider
            answer = await self.llm_provider.generate_response(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                context_details=filtered_context
            )

            # 6. Calculate Confidence
            failed_upstreams = [k for k, v in upstream_statuses.items() if v == "FAILED"]
            if failed_upstreams:
                confidence = "LOW"
            elif intent_result.confidence_score >= 0.80:
                confidence = "HIGH"
            elif intent_result.confidence_score >= 0.60:
                confidence = "MEDIUM"
            else:
                confidence = "LOW"

        return PersonalizeResponse(
            answer=answer,
            confidence=confidence,
            sourcesUsed=config.selectedContext
        )


# Singleton engine instance
personalization_engine = PersonalizationEngine()
