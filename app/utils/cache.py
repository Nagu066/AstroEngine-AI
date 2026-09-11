"""
In-memory async TTL Cache implementation for upstream microservices.
"""
import time
import asyncio
from typing import Dict, Any, Optional, Tuple


class AsyncTTLCache:
    def __init__(self, default_ttl_seconds: int = 300):
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._default_ttl = default_ttl_seconds
        self._lock = asyncio.Lock()
        self._hits = 0
        self._misses = 0

    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            if key not in self._cache:
                self._misses += 1
                return None
            
            value, expires_at = self._cache[key]
            if time.time() > expires_at:
                del self._cache[key]
                self._misses += 1
                return None
            
            self._hits += 1
            return value

    async def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        async with self._lock:
            ttl = ttl_seconds if ttl_seconds is not None else self._default_ttl
            expires_at = time.time() + ttl
            self._cache[key] = (value, expires_at)

    async def clear(self) -> None:
        async with self._lock:
            self._cache.clear()

    async def get_stats(self) -> Dict[str, Any]:
        async with self._lock:
            now = time.time()
            valid_keys = sum(1 for _, exp in self._cache.values() if exp > now)
            return {
                "total_items": len(self._cache),
                "active_items": valid_keys,
                "hits": self._hits,
                "misses": self._misses,
                "hit_ratio": round(self._hits / (self._hits + self._misses), 2) if (self._hits + self._misses) > 0 else 0.0
            }


# Global cache singleton instance
global_cache = AsyncTTLCache()
