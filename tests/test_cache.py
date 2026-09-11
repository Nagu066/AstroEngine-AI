"""
Unit tests for Async TTL Cache.
"""
import pytest
import asyncio
from app.utils.cache import AsyncTTLCache


@pytest.mark.asyncio
async def test_ttl_cache_set_and_get():
    cache = AsyncTTLCache(default_ttl_seconds=10)
    await cache.set("user:101", {"name": "Aarav"})
    val = await cache.get("user:101")
    assert val == {"name": "Aarav"}
    
    stats = await cache.get_stats()
    assert stats["hits"] == 1
    assert stats["misses"] == 0


@pytest.mark.asyncio
async def test_ttl_cache_expiry():
    cache = AsyncTTLCache(default_ttl_seconds=1)
    await cache.set("temp_key", "value", ttl_seconds=1)
    
    # Wait for expiry
    await asyncio.sleep(1.1)
    val = await cache.get("temp_key")
    assert val is None
    
    stats = await cache.get_stats()
    assert stats["misses"] == 1
