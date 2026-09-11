"""
Async Upstream Client Manager for fetching User, Kundli, Horoscope, and Panchang microservices.
Features:
- Concurrent fetching via asyncio.gather
- In-memory TTL Caching
- Configurable Timeouts & Retries
- Graceful Partial Failure handling with fallbacks
"""
import asyncio
import httpx
from typing import Dict, Any, Tuple, Optional
from app.config import settings
from app.utils.cache import global_cache, AsyncTTLCache
from app.utils.logger import logger, log_latency
from app.upstream.mock_services import (
    get_mock_user,
    get_mock_kundli,
    get_mock_horoscope,
    get_mock_panchang
)
from app.models.domain import UserProfile, KundliData, HoroscopeData, PanchangData


class UpstreamClientManager:
    def __init__(self, cache: Optional[AsyncTTLCache] = None):
        self.cache = cache or global_cache

    async def _fetch_with_retry(
        self,
        client: httpx.AsyncClient,
        url: str,
        service_name: str,
        fallback_func
    ) -> Tuple[Dict[str, Any], str]:
        """
        Fetches an upstream HTTP URL with timeout and exponential backoff retry.
        Falls back to local mock data if external server is unreachable or fails.
        """
        timeout = settings.UPSTREAM_TIMEOUT_SECONDS
        max_retries = settings.UPSTREAM_MAX_RETRIES

        for attempt in range(1, max_retries + 1):
            try:
                response = await client.get(url, timeout=timeout)
                if response.status_code == 200:
                    return response.json(), "SUCCESS"
                logger.warning(f"Upstream {service_name} returned status {response.status_code} on attempt {attempt}")
            except Exception as exc:
                logger.warning(f"Upstream {service_name} fetch failed on attempt {attempt}: {exc}")
            
            if attempt < max_retries:
                await asyncio.sleep(0.1 * (2 ** (attempt - 1)))

        # Fall back gracefully to mock implementation if remote service is unavailable
        logger.info(f"Using mock fallback for upstream service: {service_name}")
        return fallback_func(), "FALLBACK_MOCK"

    async def fetch_all_context(self, user_id: str) -> Tuple[Dict[str, Any], Dict[str, str]]:
        """
        Concurrently fetches context from all 4 upstream services using asyncio.gather.
        Returns:
            - Combined context dictionary: {"user": ..., "kundli": ..., "horoscope": ..., "panchang": ...}
            - Upstream status dictionary: {"user": "SUCCESS", "kundli": "CACHE_HIT", ...}
        """
        user_cache_key = f"user:{user_id}"
        kundli_cache_key = f"kundli:{user_id}"
        horoscope_cache_key = f"horoscope:{user_id}"
        panchang_cache_key = "panchang:latest"

        # Check Cache
        cached_user = await self.cache.get(user_cache_key)
        cached_kundli = await self.cache.get(kundli_cache_key)
        cached_horoscope = await self.cache.get(horoscope_cache_key)
        cached_panchang = await self.cache.get(panchang_cache_key)

        context: Dict[str, Any] = {}
        statuses: Dict[str, str] = {}

        if cached_user:
            context["user"] = cached_user
            statuses["user"] = "CACHE_HIT"
        if cached_kundli:
            context["kundli"] = cached_kundli
            statuses["kundli"] = "CACHE_HIT"
        if cached_horoscope:
            context["horoscope"] = cached_horoscope
            statuses["horoscope"] = "CACHE_HIT"
        if cached_panchang:
            context["panchang"] = cached_panchang
            statuses["panchang"] = "CACHE_HIT"

        # Build async tasks for missing items
        tasks = []
        task_names = []

        async with httpx.AsyncClient() as client:
            if "user" not in context:
                url = f"{settings.USER_SERVICE_URL}/{user_id}"
                tasks.append(self._fetch_with_retry(client, url, "User Service", lambda: get_mock_user(user_id)))
                task_names.append("user")

            if "kundli" not in context:
                url = f"{settings.KUNDLI_SERVICE_URL}/{user_id}"
                tasks.append(self._fetch_with_retry(client, url, "Kundli Service", lambda: get_mock_kundli(user_id)))
                task_names.append("kundli")

            if "horoscope" not in context:
                url = f"{settings.HOROSCOPE_SERVICE_URL}/{user_id}"
                tasks.append(self._fetch_with_retry(client, url, "Horoscope Service", lambda: get_mock_horoscope(user_id)))
                task_names.append("horoscope")

            if "panchang" not in context:
                url = settings.PANCHANG_SERVICE_URL
                tasks.append(self._fetch_with_retry(client, url, "Panchang Service", get_mock_panchang))
                task_names.append("panchang")

            if tasks:
                with log_latency(f"Upstream Concurrent Fetch for user={user_id}"):
                    results = await asyncio.gather(*tasks, return_exceptions=True)

                for name, result in zip(task_names, results):
                    if isinstance(result, Exception):
                        logger.error(f"Partial failure fetching {name}: {result}")
                        statuses[name] = "FAILED"
                        # Set minimal fallback or None for partial failure handling
                        context[name] = None
                    else:
                        data, status = result
                        context[name] = data
                        statuses[name] = status
                        
                        # Populate Cache
                        cache_key = f"{name}:{user_id}" if name != "panchang" else panchang_cache_key
                        await self.cache.set(cache_key, data, settings.UPSTREAM_CACHE_TTL_SECONDS)

        return context, statuses
