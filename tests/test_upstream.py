"""
Unit tests for Upstream Client Manager and concurrent fetching.
"""
import pytest
from app.upstream.client import UpstreamClientManager
from app.utils.cache import AsyncTTLCache


@pytest.mark.asyncio
async def test_concurrent_upstream_fetching():
    test_cache = AsyncTTLCache()
    client_manager = UpstreamClientManager(cache=test_cache)
    
    context, statuses = await client_manager.fetch_all_context("user_101")
    
    assert "user" in context
    assert "kundli" in context
    assert "horoscope" in context
    assert "panchang" in context
    assert context["user"]["id"] == "user_101"
    assert context["kundli"]["lagna"] == "Libra"

    # Verify second call hits cache
    context2, statuses2 = await client_manager.fetch_all_context("user_101")
    assert statuses2["user"] == "CACHE_HIT"
    assert statuses2["kundli"] == "CACHE_HIT"
